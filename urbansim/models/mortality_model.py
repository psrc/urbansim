# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import where

class MortalityModel(AgentRelocationModel):
    """
    """
    model_name = "Mortality Model"

    def run(self, person_set, household_set, resources=None):
        person_ds_name = person_set.get_dataset_name()
        hh_ds_name = household_set.get_dataset_name()
        
        index = AgentRelocationModel.run(self, person_set, resources=resources)

        logger.log_status("Removing %s records from %s dataset" % (index.size, person_set.get_dataset_name()) )
        person_set.remove_elements(index)
        
        ##remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
            household_set.remove_elements(index_hh0persons)
