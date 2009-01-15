#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from numpy import where, concatenate
from opus_core.choice_model import ChoiceModel
from opus_core.logger import logger
from opus_core.misc import unique_values

class AgentRelocationChoiceModel(ChoiceModel):
    """Chooses agents for relocation according to results from a logit model plus
    all agents that are unplaced. 
    The run method returns indices of the chosen agents.
    """
    
    model_name = "Agent Relocation Choice Model"

    def __init__(self, choice_set=[0,1], location_id_name="grid_id", **kwargs):
        self.location_id_name = location_id_name
        ChoiceModel.__init__(self, choice_set, **kwargs)


    def run(self, specification, coefficients, agent_set, **kwargs):
        choices = ChoiceModel.run(self, specification, coefficients, agent_set, **kwargs)
        movers_indices = where(choices>0)[0]
        # add unplaced agents
        unplaced_agents = where(agent_set.get_attribute(self.location_id_name) <= 0)[0]
        logger.log_status("%s agents selected by the logit model; %s agents without %s." % 
                          (movers_indices.size, unplaced_agents.size, self.location_id_name))
        movers_indices = unique_values(concatenate((movers_indices, unplaced_agents)))
        logger.log_status("Number of movers: " + str(movers_indices.size), 2)
        return movers_indices
