# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.misc import DebugPrinter, unique
from opus_core.upc_factory import UPCFactory
from opus_core.logger import logger
from opus_core.resources import Resources, merge_resources_if_not_None
from opus_core.model import Model
from numpy import where, array, concatenate, asarray, resize
from urbansim.models.rate_based_model import RateBasedModel

class AgentRelocationModel(RateBasedModel):
    """Chooses agents for relocation (according to probabilities computed by the probabilities class),
    such as employment relocation model, household relocation model. If probabilities is set to None, only unplaced agents are chosen.
    The run method returns indices of the chosen agents.
    """

    def __init__(self,
                 model_name = "Agent Relocation Model",
                 location_id_name="grid_id",
                 **kwargs
                 ):
        
        self.location_id_name = location_id_name
        RateBasedModel.__init__(self, model_name=model_name, 
                                **kwargs)
        
    def run(self, agent_set, 
            append_unplaced_agents_index=True,
            **kwargs):
        movers_indices = RateBasedModel.run(self, agent_set, **kwargs)
        if (agent_set.size() > 0) and append_unplaced_agents_index:
            # add unplaced agents
            unplaced_agents = where(agent_set.get_attribute(self.location_id_name) <= 0)[0]
            movers_indices = unique(concatenate((movers_indices, unplaced_agents)))
        
        logger.log_status("Number of total movers: " + str(movers_indices.size))
        return movers_indices


### In order to remove a circular dependency between this file and
### household_location_choice_model_creator, these unit tests were moved into
### urbansim.tests.test_agent_relocation_model.