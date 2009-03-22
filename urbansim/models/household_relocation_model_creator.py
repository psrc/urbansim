# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import merge_resources_if_not_None
from urbansim.models.agent_relocation_model import AgentRelocationModel

class HouseholdRelocationModelCreator(object):
    def get_model(self, choices = "opus_core.random_choices", 
            probabilities = "urbansim.household_relocation_probabilities", 
            location_id_name = "grid_id",
            debuglevel=0):
        return AgentRelocationModel(probabilities = probabilities,
                                    choices = choices,
                                    location_id_name = location_id_name,
                                    model_name="Household Relocation Model",
                                    debuglevel=debuglevel)
        