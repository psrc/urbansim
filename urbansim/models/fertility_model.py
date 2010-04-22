# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from numpy import ones, arange
from numpy.random import randint

class FertilityModel(AgentRelocationModel):
    """
    """
    model_name = "Fertility Model"

    def run(self, person_set, household_set, resources=None):
        index = AgentRelocationModel.run(self, person_set, resources=resources)

        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = person_set.get_dataset_name(), household_set.get_id_name()[0]
        
        max_person_id = person_set.get_attribute(person_id_name).max() + 1
        new_person_id = arange(max_person_id, max_person_id+index.size)
        
        new_born = {}
        new_born[person_id_name] = new_person_id
        new_born[hh_id_name] = person_set.get_attribute(hh_id_name)[index]
        new_born['age'] = ones(index.size, dtype="int32")
        ##TODO: give better default values
        new_born['sex'] = randint(2, size=index.size)  ##TODO: better way to assign sex?
        #new_born['education']
        #new_born['job_id']
        #new_born['race_id'] 
        #new_born['relation']
        
        person_set.add_elements(data=new_born, change_ids_if_not_unique=True) 
        
        