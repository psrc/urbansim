# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import where, array

class MortalityModel(AgentRelocationModel):
    """
    """
    model_name = "Mortality Model"

    def run(self, person_set, household_set, resources=None):
        person_ds_name = person_set.get_dataset_name()
        hh_ds_name = household_set.get_dataset_name()
        index = AgentRelocationModel.run(self, person_set, resources=resources)

        ##Preventing adults who are the only adult in a household with children from dying (to limit the number of orphans). Orphans will still be created when, in a single year, all adults die in a multiple-adult household.  In the future, perhaps an adoption model could be used or orphans could just be randomly allocated to other households.
        single_parent = person_set.compute_variables("(person.disaggregate(household.children>0)*1) * ((person.disaggregate(household.aggregate(person.age>17)) == 1)*1) * ((person.age>17)*1)", resources=resources)[index]
        index_can_die = where(single_parent==0)[0]
        logger.log_status("Removing %s records from %s dataset" % (index_can_die.size, person_set.get_dataset_name()) )
        person_set.remove_elements(index_can_die)
        
        ##remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
            household_set.remove_elements(index_hh0persons)

        ##Update the household table's persons attribute to account for deaths
        if 'persons' in household_set.get_primary_attribute_names():
            persons = household_set.compute_variables('_persons = household.number_of_agents(person)')
            household_set.modify_attribute('persons', persons)
        ##Update the household table's children attribute to account for child deaths
        if 'children' in household_set.get_primary_attribute_names():
            children = household_set.compute_variables('_children = household.aggregate(person.age<18)')
            household_set.modify_attribute('children', children)
        ##Update the household table's workers attribute to account for worker deaths
        ##For MAG, each person's work_status is coded according to the ESR variable in the 2000 PUMS. 1: employed, at work. 2: employed with a job but not at work. 4: armed forces, at work.  5: armed forces, with a job but not at work
        ##Note that the WIF variable in the 2000 PUMS (which is the source for the household table's workers attribute), only applies to workers in families and the variable is top-coded so that families with 3+ workers get a value 3.
        if 'workers' in household_set.get_primary_attribute_names():
            workers = household_set.compute_variables('_workers = household.aggregate(person.work_status == 1) + household.aggregate(person.work_status == 2) +  household.aggregate(person.work_status == 4) + household.aggregate(person.work_status == 5)')
            household_set.modify_attribute('workers', workers)
        ##If the head of the household dies, assign "head of the household" status to the person with the next lowest person_id (who will often, but not always, be the next oldest).
        ##In the base-year data, the lowest person_id in each household is always the household head.
        ##Since the fertility model assigns person_id's in order of birth, people who are born later in the simulation will have higher person_ids.
        if 'head_of_hh' in person_set.get_primary_attribute_names():
            head_of_hh = person_set.compute_variables('_head_of_hh = (person.person_id == person.disaggregate(household.aggregate(person.person_id, function=minimum)))*1')
            person_set.modify_attribute('head_of_hh', head_of_hh)
        ##Update the age_of_head attribute in the household table to reflect the age of new heads of the household and to reflect the aging of existing heads of household.
        if 'age_of_head' in household_set.get_primary_attribute_names():
            age_of_head = household_set.compute_variables('_age_of_head = household.aggregate(person.head_of_hh * person.age)')
            household_set.modify_attribute('age_of_head', age_of_head)
        ##When a person's spouse dies, change the person's marriage_status from married to widowed. (This has implications for the household formation model)
        ##Note that a marriage_status=1 is supposed to indicate being married to a spouse who resides in the same household.  In the case of marriage_status=2, which indicates married to a spouse who does not live in the household, we cannot tell when someone's spouse dies.  Widowed (marriage_status = 3) includes men.
        if 'marriage_status' in person_set.get_primary_attribute_names():
            widowed = person_set.compute_variables('_last_spouse = (((person.disaggregate(household.aggregate(person.marriage_status == 1)))==1)*1) * ((person.marriage_status == 1)*1)')
            index_widow = where(widowed==1)[0]
            if index_widow.size > 0:
                person_set.modify_attribute('marriage_status', array(index_widow.size*[3]), index_widow)