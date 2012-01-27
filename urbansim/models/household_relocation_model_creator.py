# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import merge_resources_if_not_None
from urbansim.models.agent_relocation_model import AgentRelocationModel

class HouseholdRelocationModelCreator(object):
    def get_model(self, choices = "opus_core.upc.random_choices", 
            probabilities = "opus_core.upc.rate_based_probabilities", 
            location_id_name = "grid_id",
            debuglevel=0):
        return AgentRelocationModel(probabilities = probabilities,
                                    choices = choices,
                                    location_id_name = location_id_name,
                                    model_name="Household Relocation Model",
                                    debuglevel=debuglevel)
        