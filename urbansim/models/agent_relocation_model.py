# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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
        self.debug.print_debug("Number of movers: " + str(movers_indices.size), 2)
        return movers_indices

    def prepare_for_run(self, what=None, rate_dataset_name=None, rate_storage=None, rate_table=None, 
                        sample_rates=False, n=100, multiplicator=1, flush_rates=True):
        from opus_core.datasets.dataset_factory import DatasetFactory
        from opus_core.session_configuration import SessionConfiguration
        resources = Resources()
        if (rate_storage is None) or ((rate_table is None) and (rate_dataset_name is None)):
            return resources
        if not rate_dataset_name:
            rate_dataset_name = DatasetFactory().dataset_name_for_table(rate_table)
        
        rates = DatasetFactory().search_for_dataset(rate_dataset_name,
                                                    package_order=SessionConfiguration().package_order,
                                                    arguments={'in_storage':rate_storage, 
                                                               'in_table_name':rate_table,
                                                           }
                                                    )
        
        if sample_rates:
            cache_storage=None
            if flush_rates:
                cache_storage=rate_storage
            rates.sample_rates(n=n, cache_storage=cache_storage,
                                multiplicator=multiplicator)
        resources.merge({rate_dataset_name:rates})
        return resources


### In order to remove a circular dependency between this file and
### household_location_choice_model_creator, these unit tests were moved into
### urbansim.tests.test_agent_relocation_model.