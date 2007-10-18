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

from enthought.traits.api import HasStrictTraits, Str, Int, Float, Trait

from opus_core.configuration import Configuration
from opus_core.misc import get_string_or_None

class HouseholdLocationChoiceModelConfigurationCreator(HasStrictTraits):
    agent_set = Str('household')
    debuglevel = Trait('debuglevel', Str, Int)
    sampler = Trait('opus_core.samplers.weighted_sampler', None, Str) 
    choices = Str('urbansim.lottery_choices')
    location_set = Str('gridcell')
    capacity_string = Trait('vacant_residential_units', None, Str)
    sample_size_locations = Int(30)
    portion_to_unplace = Float(1/12.0)
    nchunks = Int(12)
    agents_for_estimation_table_name = Str('households_for_estimation')
    number_of_units_string = Trait('residential_units', None, Str)
    number_of_agents_string = Trait('number_of_households', None, Str)
    lottery_max_iterations = Int(3)
    maximum_runs = Int(3)
    
    coefficients_table = Str('household_location_choice_model_coefficients')
    specification_table = Str('household_location_choice_model_specification')
    
    input_index = Str('hrm_index')
    
    _model_name = 'household_location_choice_model'
    
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
                'urbansim.models.%s' % self._model_name: 'HouseholdLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'sampler': get_string_or_None(self.sampler),
                    'choices': "'%s'" % self.choices,
                    'dataset_pool': 'dataset_pool',
                    'location_set': self.location_set,
                    'sample_size_locations': self.sample_size_locations,
                    'capacity_string': get_string_or_None(self.capacity_string),
                    'number_of_units_string': get_string_or_None(self.number_of_units_string),
                    'number_of_agents_string': get_string_or_None(self.number_of_agents_string),
                    'run_config': {'lottery_max_iterations': self.lottery_max_iterations}
                    },
                'name': 'HouseholdLocationChoiceModel'
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
        creator = HouseholdLocationChoiceModelConfigurationCreator()
        
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
                'urbansim.models.household_location_choice_model': 'HouseholdLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'sampler': "'opus_core.samplers.weighted_sampler'",
                    'choices': "'urbansim.lottery_choices'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'gridcell',
                    'sample_size_locations': 30,
                    'capacity_string': "'vacant_residential_units'",
                    'number_of_units_string': "'residential_units'",
                    'number_of_agents_string': "'number_of_households'",
                    'run_config': {'lottery_max_iterations': 3}
                    },
                'name': 'HouseholdLocationChoiceModel'
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
        creator = HouseholdLocationChoiceModelConfigurationCreator(
            agent_set = 'agent_set',
            debuglevel = 999,
            sampler = None,
            choices = 'package.choices',
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
                'urbansim.models.household_location_choice_model': 'HouseholdLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'sampler': None, 
                    'choices': "'package.choices'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'location_set',
                    'sample_size_locations': 2000,
                    'capacity_string': "'vacant_residential_units'",
                    'number_of_units_string': "'residential_units'",
                    'number_of_agents_string': "'number_of_households'",
                    'run_config': {'lottery_max_iterations': 20}
                    },
                'name': 'HouseholdLocationChoiceModel'
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