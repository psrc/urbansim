# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator as USELCMCC

class RegionalEmploymentLocationChoiceModelConfigurationCreator(USELCMCC):
    _model_name = 'regional_employment_location_choice_model'

    def __init__(self, input_index = 'erm_index', lottery_max_iterations = 5, maximum_runs = 2, *args, **kwargs):
        USELCMCC.__init__(self, 
                          input_index = input_index, 
                          lottery_max_iterations = lottery_max_iterations, 
                          maximum_runs = maximum_runs,
                          *args, **kwargs)
            
    def execute(self):
        conf = USELCMCC.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalEmploymentLocationChoiceModel'}
        conf['init']['name'] = 'RegionalEmploymentLocationChoiceModel'
        return conf

 
from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestEmploymentLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalEmploymentLocationChoiceModelConfigurationCreator()
        
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
                'washtenaw.models.regional_employment_location_choice_model': 'RegionalEmploymentLocationChoiceModel'
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
                                   'lottery_max_iterations': 5},
                     'variable_package': "'urbansim'"
                    },
                'name': 'RegionalEmploymentLocationChoiceModel'
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
                     'maximum_runs': 2
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
                
if __name__ == '__main__':
    opus_unittest.main()