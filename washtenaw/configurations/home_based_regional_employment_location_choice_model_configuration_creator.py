# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.configurations.home_based_employment_location_choice_model_configuration_creator import HomeBasedEmploymentLocationChoiceModelConfigurationCreator

class HomeBasedRegionalEmploymentLocationChoiceModelConfigurationCreator(HomeBasedEmploymentLocationChoiceModelConfigurationCreator):    
    _model_name = 'home_based_regional_employment_location_choice_model'
    
    def __init__(self, maximum_runs = 3, input_index = 'erm_index', *args, **kwargs):
        HomeBasedEmploymentLocationChoiceModelConfigurationCreator.__init__(self,
                                                                            maximum_runs = maximum_runs,
                                                                            input_index = input_index,
                                                                            *args,
                                                                            **kwargs)
    def execute(self):
        conf = HomeBasedEmploymentLocationChoiceModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.regional_employment_location_choice_model': 'RegionalEmploymentLocationChoiceModel'}
        conf['init']['name'] = 'RegionalEmploymentLocationChoiceModel'
        return conf


            

from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestHomeBasedEmploymentLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = HomeBasedRegionalEmploymentLocationChoiceModelConfigurationCreator()
        
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
                    'choices': "'urbansim.lottery_choices'",
                    'dataset_pool': 'dataset_pool',
                    'estimation_weight_string': "'residential_units'",
                    'location_set': 'gridcell',
                    'number_of_units_string': "'residential_units'",
                    'sample_size_locations': 30
                    },
                'name': 'RegionalEmploymentLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'jobs_for_estimation'",
                    'data_objects': 'datasets',
                    'portion_to_unplace': 1/12.,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'employment_location_choice_model_specification'"
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
            
if __name__ == '__main__':
    opus_unittest.main()