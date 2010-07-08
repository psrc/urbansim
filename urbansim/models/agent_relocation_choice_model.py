# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import where, concatenate, arange, rint
from opus_core.choice_model import ChoiceModel
from opus_core.logger import logger
from opus_core.misc import unique
from opus_core.sampling_toolbox import sample_noreplace

class AgentRelocationChoiceModel(ChoiceModel):
    """Chooses agents for relocation according to results from a logit model plus
    all agents that are unplaced. 
    The run method returns indices of the chosen agents.
    """
    
    model_name = "Agent Relocation Choice Model"

    def __init__(self, choice_set=[0,1], location_id_name="grid_id", movers_ratio=None, **kwargs):
        self.location_id_name = location_id_name
        self.movers_ratio = movers_ratio
        ChoiceModel.__init__(self, choice_set, **kwargs)


    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        choices = ChoiceModel.run(self, specification, coefficients, agent_set, agents_index=agents_index, **kwargs)
        if agents_index is None:
            agents_index=arange(agent_set.size())
        movers_indices = agents_index[where(choices>0)]
        if self.movers_ratio is not None:
            n = rint(self.movers_ratio*agents_index.size)
            if n < movers_indices.size:
                movers_indices = sample_noreplace(movers_indices, n)
        # add unplaced agents
        unplaced_agents = agents_index[agent_set.get_attribute_by_index(self.location_id_name, agents_index) <= 0]
        logger.log_status("%s agents selected by the logit model; %s agents without %s." % 
                          (movers_indices.size, unplaced_agents.size, self.location_id_name))
        movers_indices = unique(concatenate((movers_indices, unplaced_agents)))
        logger.log_status("Number of movers: " + str(movers_indices.size))
        return movers_indices
