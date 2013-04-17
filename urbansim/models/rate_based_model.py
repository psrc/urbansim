# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.misc import DebugPrinter
from opus_core.upc.upc_factory import UPCFactory
from opus_core.logger import logger
from opus_core.resources import merge_resources_if_not_None
from opus_core.models.model import Model
from opus_core.simulation_state import SimulationState
from numpy import where, array, asarray, resize

class RateBasedModel(Model):
    """Chooses agents for relocation (according to probabilities computed by the probabilities class).
    It includes all jobs that are unplaced. If probabilities is set to None, only unplaced agents are chosen.
    The run method returns indices of the chosen agents.
    """
    model_name = 'Rate Based Model'
    
    def __init__(self,
                 probabilities = "opus_core.upc.rate_based_probabilities",
                 choices = "opus_core.random_choices",
                 model_name = None,
                 debuglevel=0,
                 resources=None
                 ):
        if model_name is not None:
            self.model_name = model_name
        self.debug = DebugPrinter(debuglevel)
        self.upc_sequence = None
        if probabilities is not None:
            self.upc_sequence = UPCFactory().get_model(utilities=None,
                                                       probabilities=probabilities,
                                                       choices=choices,
                                                       debuglevel=debuglevel)
        self.resources = merge_resources_if_not_None(resources)
        
    def run(self, agent_set, 
            resources=None, 
            reset_attribute_value={}):
        self.resources.merge(resources)
        
        if agent_set.size()<=0:
            agent_set.get_id_attribute()
            if agent_set.size()<= 0:
                self.debug.print_debug("Nothing to be done.",2)
                return array([], dtype='int32')

        if self.upc_sequence and (self.upc_sequence.probability_class.rate_set or self.resources.get('rate_set', None)):
            self.resources.merge({agent_set.get_dataset_name():agent_set}) #to be compatible with old-style one-relocation_probabilities-module-per-model
            self.resources.merge({'agent_set':agent_set})
            choices = self.upc_sequence.run(resources=self.resources)
            # choices have value 1 for agents that should be relocated, otherwise 0.
            movers_indices = where(choices>0)[0]
        else:
            movers_indices = array([], dtype='int32')

        if reset_attribute_value and movers_indices.size > 0:
            for key, value in reset_attribute_value.items():
                agent_set.modify_attribute(name=key, 
                                           data=resize(asarray(value), movers_indices.size),
                                           index=movers_indices)            
        
        logger.log_status("Number of agents sampled based on rates: " + str(movers_indices.size))
        return movers_indices

    def prepare_for_run(self, what=None, 
                        rate_dataset_name="rate",
                        rate_storage=None, 
                        rate_table=None, 
                        probability_attribute=None,
                        sample_rates=False, 
                        n=100, 
                        multiplicator=1, 
                        flush_rates=True):
        """
        what - unused, argument kept to be compatible with old code 
        """
        from opus_core.datasets.dataset_factory import DatasetFactory
        from opus_core.session_configuration import SessionConfiguration
        
        if (rate_storage is None) or ((rate_table is None) and (rate_dataset_name is None)):
            return self.resources
        if not rate_dataset_name:
            rate_dataset_name = DatasetFactory().dataset_name_for_table(rate_table)
        
        rates = DatasetFactory().search_for_dataset(rate_dataset_name,
                                                    package_order=SessionConfiguration().package_order,
                                                    arguments={'in_storage':rate_storage, 
                                                               'in_table_name':rate_table,
                                                           }
                                                    )
        if probability_attribute is not None:
            rates.probability_attribute = probability_attribute
        if sample_rates:
            cache_storage=None
            if flush_rates:
                cache_storage=rate_storage
            rates.sample_rates(n=n, cache_storage=cache_storage,
                                multiplicator=multiplicator)
        self.resources.merge({rate_dataset_name:rates}) #to be compatible with old-style one-relocation_probabilities-module-per-model
        self.resources.merge({'rate_set':rates})
        return self.resources

### In order to remove a circular dependency between this file and
### household_location_choice_model_creator, these unit tests were moved into
### urbansim.tests.test_agent_relocation_model.
