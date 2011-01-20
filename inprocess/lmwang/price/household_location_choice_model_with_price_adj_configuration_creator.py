# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from opus_core.configuration import Configuration
from opus_core.misc import get_string_or_None

class HouseholdLocationChoiceModelWithPriceAdjConfigurationCreator(object):
    _model_name = "inprocess.lmwang.price.household_location_choice_model_with_price_adj"

    def __init__(self,
                agent_set = 'household',
                debuglevel = 'debuglevel',
                coefficients_table = 'household_location_choice_model_coefficients',
                specification_table = 'household_location_choice_model_specification',
                location_set = 'gridcell',
                sampler = 'opus_core.samplers.weighted_sampler',
                choices = 'urbansim.lottery_choices',
                capacity_string = 'vacant_residential_units',
                sample_size_locations = 30,
                portion_to_unplace = 1/12.0,
                nchunks = 12,
                agents_for_estimation_table_name = 'households_for_estimation',
                number_of_units_string = 'residential_units',
                number_of_agents_string = 'number_of_households',
                lottery_max_iterations = 3,
                maximum_runs = 5,
                estimation_procedure = 'opus_core.bhhh_mnl_estimation',
                demand_string = "demand_string",
                input_index = 'hrm_index'):
        self.agent_set = agent_set
        self.debuglevel = debuglevel
        self.coefficients_table = coefficients_table
        self.specification_table = specification_table
        self.location_set = location_set
        self.sampler = sampler
        self.choices = choices
        self.capacity_string = capacity_string
        self.sample_size_locations = sample_size_locations
        self.portion_to_unplace = portion_to_unplace
        self.nchunks = nchunks
        self.agents_for_estimation_table_name = agents_for_estimation_table_name
        self.number_of_units_string = number_of_units_string
        self.number_of_agents_string = number_of_agents_string
        self.lottery_max_iterations = lottery_max_iterations
        self.maximum_runs = maximum_runs
        self.estimation_procedure = estimation_procedure
        self.demand_string = demand_string
        self.input_index = input_index
    
    def execute(self):
        _coefficients = 'coefficients'
        _specification = 'specification'
        _index = 'index'
        
        return Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_index': _index,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'specification': _specification,
                    },
                'output': '(%s, _)' % _coefficients
                },
            'import': {
                #'urbansim.models.%s' % self._model_name: 'HouseholdLocationChoiceModelWithPriceAdj'
                self._model_name: 'HouseholdLocationChoiceModelWithPriceAdj'  #model module in current directory
                },
            'init': {
                'arguments': {
                    'sampler': get_string_or_None(self.sampler),
                    'choices': "'%s'" % self.choices,
                    'estimation': "'%s'" % self.estimation_procedure,                    
                    'dataset_pool': 'dataset_pool',
                    'location_set': self.location_set,
                    'sample_size_locations': self.sample_size_locations,
                    'capacity_string': get_string_or_None(self.capacity_string),
                    'demand_string': get_string_or_None(self.demand_string),
                    'number_of_units_string': get_string_or_None(self.number_of_units_string),
                    'number_of_agents_string': get_string_or_None(self.number_of_agents_string),
                    'run_config': {'lottery_max_iterations': self.lottery_max_iterations}
                    },
                'name': 'HouseholdLocationChoiceModelWithPriceAdj'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'%s'" % self.agents_for_estimation_table_name,
                    'data_objects': 'datasets',
                    'index_to_unplace': self.input_index,
                    'join_datasets': 'True',
                    'portion_to_unplace': self.portion_to_unplace,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    },
                'name': 'prepare_for_estimate',
                'output': '(%s, %s)' % (_specification, _index)
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'%s'" % self.coefficients_table,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    },
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_specification, _coefficients)
                },
            'run': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_index': self.input_index,
                    'chunk_specification': "{'nchunks':%s}" % self.nchunks,
                    'coefficients': _coefficients,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'specification': _specification,
                    'maximum_runs': self.maximum_runs
                    }
                }
            })


from opus_core.tests import opus_unittest 


class TestHouseholdLocationChoiceModelConfiguration(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = HouseholdLocationChoiceModelWithPriceAdjConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_index': 'index',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'household_location_choice_model_with_price_adj': 'HouseholdLocationChoiceModelWithPriceAdj'
                },
            'init': {
                'arguments': {
                    'sampler': "'opus_core.samplers.weighted_sampler'",
                    'choices': "'urbansim.lottery_choices'",
                    'estimation': "'opus_core.bhhh_mnl_estimation'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'gridcell',
                    'sample_size_locations': 30,
                    'demand_string': "'demand_string'",
                    'capacity_string': "'vacant_residential_units'",
                    'number_of_units_string': "'residential_units'",
                    'number_of_agents_string': "'number_of_households'",
                    'run_config': {'lottery_max_iterations': 3}
                    },
                'name': 'HouseholdLocationChoiceModelWithPriceAdj'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'households_for_estimation'",
                    'data_objects': 'datasets',
                    'index_to_unplace': 'hrm_index',
                    'join_datasets': 'True',
                    'portion_to_unplace': 1/12.0,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'household_location_choice_model_specification'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'household_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'household_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_index': 'hrm_index',
                    'chunk_specification': "{'nchunks':12}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification',
                    'maximum_runs': 5
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = HouseholdLocationChoiceModelWithPriceAdjConfigurationCreator(
            agent_set = 'agent_set',
            debuglevel = 999,
            sampler = None,
            choices = 'package.choices',
            estimation_procedure = 'opus_core.my_estimation_procedure',
            location_set = 'location_set',
            sample_size_locations = 2000,
            portion_to_unplace = 888.8,
            nchunks = 12345,
            agents_for_estimation_table_name = 'agents_for_estimation_table_name',
            lottery_max_iterations = 20,
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            input_index = 'input_index',
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_index': 'index',
                    'data_objects': 'datasets',
                    'debuglevel': 999,
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'household_location_choice_model_with_price_adj': 'HouseholdLocationChoiceModelWithPriceAdj'
                },
            'init': {
                'arguments': {
                    'sampler': None, 
                    'choices': "'package.choices'",
                    'estimation': "'opus_core.my_estimation_procedure'",                    
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'location_set',
                    'sample_size_locations': 2000,
                    'demand_string': "'demand_string'",
                    'capacity_string': "'vacant_residential_units'",
                    'number_of_units_string': "'residential_units'",
                    'number_of_agents_string': "'number_of_households'",
                    'run_config': {'lottery_max_iterations': 20}
                    },
                'name': 'HouseholdLocationChoiceModelWithPriceAdj'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'agents_for_estimation_table_name'", ###
                    'data_objects': 'datasets',
                    'index_to_unplace': 'input_index', 
                    'join_datasets': 'True',
                    'portion_to_unplace': 888.8,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'coefficients_table'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_index': 'input_index',
                    'chunk_specification': "{'nchunks':12345}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 999,
                    'specification': 'specification',
                    'maximum_runs': 5
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()
