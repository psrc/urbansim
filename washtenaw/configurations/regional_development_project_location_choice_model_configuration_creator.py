# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configurations.development_project_location_choice_model_configuration_creator import DevelopmentProjectLocationChoiceModelConfigurationCreator as USDPLCMCC

class RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator(USDPLCMCC):
         
    def __init__(self, records_per_chunk = 1000, *args, **kwargs):
        USDPLCMCC.__init__(self, records_per_chunk = records_per_chunk, *args, **kwargs)
        
    def execute(self):
        conf = USDPLCMCC.execute(self)
        conf['import'] = {'washtenaw.models.regional_development_project_location_choice_model': 
                              'RegionalDevelopmentProjectLocationChoiceModel'}
        conf['init']['name'] = 'RegionalDevelopmentProjectLocationChoiceModel'
        return conf


from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestDevelopmentProjectLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator(
            project_type = 'project_type',
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'projects',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'washtenaw.models.regional_development_project_location_choice_model': 'RegionalDevelopmentProjectLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'location_set': 'gridcell',
                    'model_configuration': "model_configuration['development_project_types']['project_type']",
                    'project_type': "'project_type'",
                    'submodel_string': "'size_category'"
                    },
                'name': 'RegionalDevelopmentProjectLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'base_year': "resources['base_year']",
                    'categories': "model_configuration['development_project_types']['project_type']['categories']",
                    'events_for_estimation_storage': 'base_cache_storage',
                    'events_for_estimation_table': "'development_event_history'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'project_type_development_location_choice_model_specification'",
                    'urbansim_constant': 'urbansim_constant'
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, projects)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'project_type_development_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'project_type_development_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': "dptm_results['project_type']",
                    'chunk_specification': "{'records_per_chunk':1000}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
                    
if __name__ == '__main__':
    opus_unittest.main()