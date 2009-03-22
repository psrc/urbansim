# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration
from opus_core.misc import get_string_or_None

class EmploymentLocationChoiceModelConfigurationCreator(object):
    
    _model_name = 'employment_location_choice_model'
    
    def __init__(self,
                agent_set = 'job',
                sample_size_locations = 30,
                debuglevel = 'debuglevel',
                sampler = 'opus_core.samplers.weighted_sampler',
                choices = 'urbansim.lottery_choices',
                location_set = 'gridcell',
                portion_to_unplace = 1/12.0,
                records_per_chunk = 50000,
                attribute_to_group_by = 'job_building_type.name',
                agents_for_estimation_table = 'jobs_for_estimation',
                join_datasets = False,
                filter_for_estimation = None,
                filter = None,
                capacity_string = 'vacant_SSS_job_space',
                compute_capacity_flag = True,
                estimation_weight_string = 'total_number_of_possible_SSS_jobs',
                simulation_weight_string = None, # if this is None, weights are proportional to the capacity 
                estimation_size_agents = 1.0,
                agent_units_string = None,
                number_of_units_string = 'total_number_of_possible_SSS_jobs',
                lottery_max_iterations = 3,
                variable_package = "urbansim",
                maximum_runs = 3,
                input_index = 'erm_index',
                estimation_procedure = 'opus_core.bhhh_mnl_estimation',
                coefficients_table = 'employment_location_choice_model_coefficients',
                specification_table = 'employment_location_choice_model_specification'):
        self.agent_set = agent_set
        self.sample_size_locations = sample_size_locations
        self.debuglevel = debuglevel
        self.sampler = sampler
        self.choices = choices
        self.location_set = location_set
        self.portion_to_unplace = portion_to_unplace
        self.records_per_chunk = records_per_chunk
        self.attribute_to_group_by = attribute_to_group_by
        self.agents_for_estimation_table = agents_for_estimation_table
        self.join_datasets = join_datasets
        self.filter_for_estimation = filter_for_estimation
        self.filter = filter
        self.capacity_string = capacity_string
        self.compute_capacity_flag = compute_capacity_flag
        self.estimation_weight_string = estimation_weight_string
        self.simulation_weight_string = simulation_weight_string
        self.estimation_size_agents = estimation_size_agents
        self.agent_units_string = agent_units_string
        self.number_of_units_string = number_of_units_string
        self.lottery_max_iterations = lottery_max_iterations
        self.variable_package = variable_package
        self.maximum_runs = maximum_runs
        self.input_index = input_index
        self.estimation_procedure = estimation_procedure
        self.coefficients_table = coefficients_table
        self.specification_table = specification_table
        
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
                    'sampler': get_string_or_None(self.sampler),
                    'choices': "'%s'" % self.choices,
                    'estimation': "'%s'" % self.estimation_procedure,
                    'dataset_pool': 'dataset_pool',
                    'location_set': self.location_set,
                    'sample_size_locations': self.sample_size_locations,
                    'capacity_string': get_string_or_None(self.capacity_string),
                    'estimation_weight_string': get_string_or_None(self.estimation_weight_string),
                    'simulation_weight_string': get_string_or_None(self.simulation_weight_string),
                    'filter': get_string_or_None(self.filter),
                    'estimation_size_agents': self.estimation_size_agents,
                    'compute_capacity_flag': self.compute_capacity_flag,
                    'number_of_units_string': get_string_or_None(self.number_of_units_string), 
                    'run_config': {'agent_units_string': get_string_or_None(self.agent_units_string),
                                   'lottery_max_iterations': self.lottery_max_iterations},
                    'variable_package': "'%s'" % self.variable_package
                    },
                'name': 'EmploymentLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': get_string_or_None(self.agents_for_estimation_table),
                    'join_datasets':self.join_datasets,
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
                    'maximum_runs': self.maximum_runs
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
                    'sampler': "'opus_core.samplers.weighted_sampler'",
                    'choices': "'urbansim.lottery_choices'",
                    'estimation': "'opus_core.bhhh_mnl_estimation'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'gridcell',
                    'sample_size_locations': 30,
                    'capacity_string': "'vacant_SSS_job_space'",
                    'estimation_weight_string': "'total_number_of_possible_SSS_jobs'",
                    'simulation_weight_string': None,
                    'filter': None,
                    'estimation_size_agents': 1.,
                    'compute_capacity_flag': True,
                    'number_of_units_string': "'total_number_of_possible_SSS_jobs'",
                    'run_config': {'agent_units_string': None,
                                   'lottery_max_iterations': 3},
                    'variable_package': "'urbansim'"
                    },
                'name': 'EmploymentLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'jobs_for_estimation'",
                    'join_datasets': False,
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
                    'specification': 'specification',
                    'maximum_runs': 3
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
            sampler = None,
            choices = 'package.choices',
            estimation_procedure = 'opus_core.my_estimation_procedure',
            location_set = 'location_set',
            portion_to_unplace = 7777.7,
            records_per_chunk = 6666,
            lottery_max_iterations = 20,
            attribute_to_group_by = 'dataset_name.attribute_name',
            agents_for_estimation_table = 'agents_for_estimation_table',
            coefficients_table = 'coefficients_table',
            specification_table = 'specification_table',
            input_index = 'input_index',
            compute_capacity_flag = False
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
                    'sampler': None, 
                    'choices': "'package.choices'",
                    'estimation': "'opus_core.my_estimation_procedure'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'location_set',
                    'sample_size_locations': 9999,
                    'capacity_string': "'vacant_SSS_job_space'",
                    'estimation_weight_string': "'total_number_of_possible_SSS_jobs'",
                    'simulation_weight_string': None,
                    'filter': None,
                    'estimation_size_agents': 1.,
                    'compute_capacity_flag': False,
                    'number_of_units_string': "'total_number_of_possible_SSS_jobs'",
                    'run_config': {'agent_units_string': None,
                                   'lottery_max_iterations': 20},
                    'variable_package': "'urbansim'"
                    },
                'name': 'EmploymentLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'agents_for_estimation_table'",
                    'join_datasets': False,
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
                    'specification': 'specification',
                    'maximum_runs': 3
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()