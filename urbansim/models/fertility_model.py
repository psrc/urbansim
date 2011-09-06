# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from numpy import zeros, arange
from numpy.random import randint
from opus_core.logger import logger

class FertilityModel(AgentRelocationModel):
    """
    """
    model_name = "Fertility Model"

    def run(self, person_set, household_set, resources=None):
        index = AgentRelocationModel.run(self, person_set, resources=resources)

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
            new_born['person_no'] = person_set.compute_variables("person.disaggregate(household.aggregate(person.person_no, function=max)) + 1")[index]
        new_born['race'] = person_set.compute_variables("person.disaggregate(household.aggregate(person.head_of_hh*person.race))")[index]
        new_born['age'] = zeros(index.size, dtype="int32")
        new_born['gender'] = randint(1, 3, size=index.size)  ##TODO: better way to assign sex?
        ##TODO: give better default values
        #new_born['education']
        #new_born['job_id']
        #new_born['relation']

        logger.log_status("Adding %s records to %s dataset" % (index.size, person_set.get_dataset_name()) )
        person_set.add_elements(data=new_born, require_all_attributes=False, change_ids_if_not_unique=True) 
        
        ##TODO: for each household that experiences a birth, increase household.persons and household.children by 1
        ##A better way is to make household.persons and household.children computed variables, instead of primary ones
        persons = household_set.compute_variables('_persons = household.number_of_agents(person)')
        children = household_set.compute_variables('_childrens = household.aggregate(person.age<18)')
        household_set.modify_attribute('persons', persons)
        household_set.modify_attribute('children', children)
       
