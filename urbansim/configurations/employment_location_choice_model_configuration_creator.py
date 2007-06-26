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

class EmploymentLocationChoiceModelConfigurationCreator(HasStrictTraits):
    agent_set = Str('job')
    sample_size_locations = Int(30)
    debuglevel = Trait('debuglevel', Str, Int)
    choices = Str('urbansim.lottery_choices')
    location_set = Str('gridcell')
    portion_to_unplace = Float(1/12.)
    records_per_chunk = Int(50000)
    attribute_to_group_by = Str('job_building_type.name')
    agents_for_estimation_table = Trait('jobs_for_estimation', None, Str)
    filter_for_estimation = Trait(None, None, Str)
    filter = Trait(None, None, Str)
    capacity_string = Trait('vacant_SSS_job_space', None, Str)
    estimation_weight_string = Trait('total_number_of_possible_SSS_jobs', None, Str)
    estimation_size_agents = Float(1.)
    
    input_index = Str('erm_index')
    
    coefficients_table = Str('employment_location_choice_model_coefficients')
    specification_table = Str('employment_location_choice_model_specification')
    
    _model_name = 'employment_location_choice_model'
    
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _coefficients = 'coefficients'
        _specification = 'specification'
        _index = 'index'
                
        try:
            attribute_to_group_by_dataset_name, attribute_to_group_by_attribute_name = self.attribute_to_group_by.split('.')
        except:
            raise Exception("Attribute to group by must be of the form "
                "'dataset_name.attribute_name', where dataset_name is the name "
                "of the dataset containing the attribute to group by "
                "(attribute_name). Received '%s'." % self.attribute_to_group_by)
        
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
            'group_by_attribute': (attribute_to_group_by_dataset_name, attribute_to_group_by_attribute_name),
            'import': {
                'urbansim.models.%s' % self._model_name: 'EmploymentLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'choices': "'%s'" % self.choices,
                    'dataset_pool': 'dataset_pool',
                    'location_set': self.location_set,
                    'sample_size_locations': self.sample_size_locations,
                    'capacity_string': get_string_or_None(self.capacity_string),
                    'estimation_weight_string': get_string_or_None(self.estimation_weight_string),
                    'filter': get_string_or_None(self.filter),
                    'estimation_size_agents': self.estimation_size_agents
                    },
                'name': 'EmploymentLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': get_string_or_None(self.agents_for_estimation_table),
                    'data_objects': 'datasets',
                    'portion_to_unplace': self.portion_to_unplace,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'%s'" % self.specification_table,
                    'filter': get_string_or_None(self.filter_for_estimation),
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
                    'chunk_specification': "{'records_per_chunk':%s}" % self.records_per_chunk,
                    'coefficients': _coefficients,
                    'data_objects': 'datasets',
                    'debuglevel': self.debuglevel,
                    'specification': _specification,
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestEmploymentLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = EmploymentLocationChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_index': 'index',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'group_by_attribute': ('job_building_type', 'name'),
            'import': {
                'urbansim.models.employment_location_choice_model': 'EmploymentLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'choices': "'urbansim.lottery_choices'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'gridcell',
                    'sample_size_locations': 30,
                    'capacity_string': "'vacant_SSS_job_space'",
                    'estimation_weight_string': "'total_number_of_possible_SSS_jobs'",
                    'filter': None,
                    'estimation_size_agents': 1.
                    },
                'name': 'EmploymentLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'jobs_for_estimation'",
                    'data_objects': 'datasets',
                    'portion_to_unplace': 1/12.,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'employment_location_choice_model_specification'",
                    'filter': None
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'employment_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'employment_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_index': 'erm_index',
                    'chunk_specification': "{'records_per_chunk':50000}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = EmploymentLocationChoiceModelConfigurationCreator(
            agent_set = 'agent_set',
            sample_size_locations = 9999,
            debuglevel = 8888,
            choices = 'package.choices',
            location_set = 'location_set',
            portion_to_unplace = 7777.7,
            records_per_chunk = 6666,
            attribute_to_group_by = 'dataset_name.attribute_name',
            agents_for_estimation_table = 'agents_for_estimation_table',
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
                    'debuglevel': 8888,
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'group_by_attribute': ('dataset_name', 'attribute_name'),
            'import': {
                'urbansim.models.employment_location_choice_model': 'EmploymentLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'choices': "'package.choices'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'location_set',
                    'sample_size_locations': 9999,
                    'capacity_string': "'vacant_SSS_job_space'",
                    'estimation_weight_string': "'total_number_of_possible_SSS_jobs'",
                    'filter': None,
                    'estimation_size_agents': 1.
                    },
                'name': 'EmploymentLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'agents_for_estimation_table'",
                    'data_objects': 'datasets',
                    'portion_to_unplace': 7777.7,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'specification_table'",
                    'filter': None
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
                    'chunk_specification': "{'records_per_chunk':6666}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 8888,
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()