# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configurations.development_project_transition_model_configuration_creator import DevelopmentProjectTransitionModelConfigurationCreator

class RegionalDevelopmentProjectTransitionModelConfigurationCreator(DevelopmentProjectTransitionModelConfigurationCreator):

    _model_name = 'development_project_transition_model'
    def execute(self):
        conf = DevelopmentProjectTransitionModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.regional_development_project_transition_model': 
                              'RegionalDevelopmentProjectTransitionModel'}
        conf['init']['name'] = 'RegionalDevelopmentProjectTransitionModel'
        return conf


from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestDevelopmentProjectTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalDevelopmentProjectTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'washtenaw.models.regional_development_project_transition_model': 'RegionalDevelopmentProjectTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 4},
                'name': 'RegionalDevelopmentProjectTransitionModel'
                },
            'run': {
                'arguments': {
                    'history_table': 'development_event_history',
                    'location_set': 'gridcell',
                    'model_configuration': 'model_configuration',
                    'resources': 'model_resources',
                    'vacancy_table': 'target_vacancy',
                    'year': 'year',
                    'resources': None
                    },
                'output': 'dptm_results'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
                    
if __name__ == '__main__':
    opus_unittest.main()