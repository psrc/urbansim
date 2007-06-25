#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.misc import DebugPrinter, unique_values
from opus_core.upc_factory import UPCFactory
from opus_core.resources import Resources
from opus_core.model import Model
from numpy import where, array, concatenate

class AgentRelocationModel(Model):
    """Chooses agents for relocation (according to probabilities computed by the probabilities class).
    It includes all jobs that are unplaced. If probabilities is set to None, only unplaced agents are chosen.
    The run method returns indices of the chosen agents.
    """

    def __init__(self,
                 probabilities = None,
                 choices = "opus_core.random_choices",
                 location_id_name="grid_id",
                 model_name = "Agent Relocation Model",
                 debuglevel=0):

        self.model_name = model_name
        self.location_id_name = location_id_name
        self.debug = DebugPrinter(debuglevel)
        self.upc_sequence = None
        if probabilities is not None:
            self.upc_sequence = UPCFactory().get_model(utilities=None,
                                                    probabilities=probabilities,
                                                    choices=choices,
                                                    debuglevel=debuglevel)


    def run(self, agent_set, resources=None):
        if not isinstance(resources, Resources):
            resources = Resources()
        if agent_set.size()<=0:
            agent_set.get_id_attribute()
            if agent_set.size()<= 0:
                self.debug.print_debug("Nothing to be done.",2)
                return array([], dtype='int32')

        if self.upc_sequence:
            resources.merge({agent_set.get_dataset_name():agent_set})
            choices = self.upc_sequence.run(resources=resources)
            # choices have value 1 for agents that should be relocated, otherwise 0.
            movers_indices = where(choices>0)[0]
        else:
            movers_indices = array([], dtype='int32')
        # add unplaced agents
        unplaced_agents = where(agent_set.get_attribute(self.location_id_name) <= 0)[0]
        movers_indices = unique_values(concatenate((movers_indices, unplaced_agents)))
        self.debug.print_debug("Number of movers: " + str(movers_indices.size), 3)
        return movers_indices

    def prepare_for_run(self, what=None, rate_storage=None, rate_table=None, sample_rates=False,
                        n=100, multiplicator=1, flush_rates=True):
        from urbansim.datasets.rate_dataset import RateDataset
        resources = Resources()
        if (rate_storage is not None) and (rate_table is not None):
            rates = RateDataset(what=what, in_storage=rate_storage,
                             in_table_name=rate_table)
            if sample_rates:
                cache_storage=None
                if flush_rates:
                    cache_storage=rate_storage
                rates.sample_rates(n=n, cache_storage=cache_storage,
                                    multiplicator=multiplicator)
            resources.merge({rates.get_dataset_name():rates})
        return resources


### In order to remove a circular dependency between this file and
### household_location_choice_model_creator, these unit tests were moved into
### urbansim.tests.test_agent_relocation_model.