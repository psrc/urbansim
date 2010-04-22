# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import where, arange

class ChildLeavingHomeModel(AgentRelocationModel):
    """
    """
    model_name = "Child Leaving Home Model"

    def run(self, person_set, household_set, resources=None):
        index = AgentRelocationModel.run(self, person_set, resources=resources)
        
        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = person_set.get_dataset_name(), household_set.get_id_name()[0]
        
        max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
        new_hh_id = arange(max_hh_id, max_hh_id+index.size)
        person_set.modify_attribute(hh_id_name, new_hh_id, index=index)
        household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
        
        logger.log_status("%s children leave home and form new %s." % (index.size, hh_ds_name) )
        
        ##remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
            household_set.remove_elements(index_hh0persons)
      