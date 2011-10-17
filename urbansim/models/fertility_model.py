# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from numpy import zeros, arange, where, array
from numpy.random import randint
from opus_core.logger import logger

class FertilityModel(AgentRelocationModel):
    """
    """
    model_name = "Fertility Model"

    def run(self, person_set, household_set, resources=None):
        index = AgentRelocationModel.run(self, person_set, resources=resources)
        logger.log_status("%s births occurred" % (index.size) )

        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = person_set.get_dataset_name(), household_set.get_id_name()[0]

        max_person_id = person_set[person_id_name].max() + 1
        new_person_id = arange(max_person_id, max_person_id+index.size)
        
        new_born = {}
        new_born[person_id_name] = new_person_id
        new_born[hh_id_name] = person_set[hh_id_name][index]
        ## this may not generate unique person_no, as person can be deleted from a households
        #new_born['person_no'] = person_set.compute_variables("person.disaggregate(household.persons) + 1")[index]
        if 'person_no' in person_set.get_known_attribute_names():
            ## this requires person_no to exist, which may not always be the case
            new_born['person_no'] = person_set.compute_variables("person.disaggregate(household.aggregate(person.person_no, function=maximum)) + 1")[index]
        #assign new-born the race of the mother
        new_born['race'] = person_set['race'][index]
        new_born['age'] = zeros(index.size, dtype="int32")
        if 'gender' in person_set.get_known_attribute_names():
            new_born['gender'] = randint(1, 3, size=index.size)
        if 'sex' in person_set.get_known_attribute_names():
            new_born['sex'] = randint(1, 3, size=index.size)  ##TODO: better way to assign sex?
        ##TODO: give better default values
        #new_born['education']
        #new_born['job_id']
        #new_born['relation']

        logger.log_status("Adding %s records to %s dataset" % (index.size, person_set.get_dataset_name()) )
        person_set.add_elements(data=new_born, require_all_attributes=False, change_ids_if_not_unique=True) 
        marriage_status0 = person_set.compute_variables("person.marriage_status == 0")
        marriage_status0_index = where(marriage_status0 == 1)[0]
        logger.log_status("%s persons have marriage_status = 0. Will be changed to marriage_status = 6" % (marriage_status0_index.size) )
        person_set.modify_attribute('marriage_status', array(marriage_status0_index.size*[6]), marriage_status0_index)  
        
        ##TODO: for each household that experiences a birth, increase household.persons and household.children by 1
        ##A better way is to use household.persons and household.children as computed variables, instead of primary ones
        if 'persons' in household_set.get_primary_attribute_names():
            persons = household_set.compute_variables('_persons = household.number_of_agents(person)')
            household_set.modify_attribute('persons', persons)

        if 'children' in household_set.get_primary_attribute_names():
            children = household_set.compute_variables('_childrens = household.aggregate(person.age<18)')
            household_set.modify_attribute('children', children)
        
        ##preventing households that experience multiple births in the same year from having newborns with duplicate person_no
        ##right now, this is a work in progress because households with 3 or more births in a single year (very rare) will still have duplicate person_no
        if 'person_no' in person_set.get_known_attribute_names():
            num_max_person_no = household_set.compute_variables('_num_max_person_no = household.aggregate(person.person_no == person.disaggregate(household.aggregate(person.person_no, function=maximum)))')
            max_person_id = person_set.compute_variables('_max_person_id = person.person_id == person.disaggregate(household.aggregate(person.person_id, function=maximum))')
            person_no_to_change = person_set.compute_variables('_to_change = person._max_person_id * person.disaggregate(household._num_max_person_no>1)')
            index_to_change = where(person_no_to_change==1)[0]
            if index_to_change.size > 0:
                person_set.modify_attribute('person_no', person_set.get_attribute('person_no')[index_to_change] + 1, index_to_change)
            
            
            
       
