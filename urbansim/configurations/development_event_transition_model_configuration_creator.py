# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array

from opus_core.configuration import Configuration


class DevelopmentEventTransitionModelConfigurationCreator(object):
    _model_name = 'development_event_transition_model'
    
    def __init__(self,
        debuglevel = 'debuglevel',
        input_projects = 'dptm_results',
        output_events = 'development_events'):
        
        self.debuglevel = debuglevel
        self.input_projects = input_projects
        self.output_events = output_events
    
    
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _types = 'all_project_types'
        _units = 'all_project_units'
        
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'prepare_for_run': {
                'arguments': {
                    'dev_projects': self.input_projects,
                    'model_configuration': 'model_configuration'
                    },
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_types, _units)
                },
            'run': {
                'arguments': {
                    'debuglevel': self.debuglevel,
                    'projects': self.input_projects,
                    'types': _types,
                    'units': _units,
                    'year': 'year'
                    },
                'output': self.output_events,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestDevelopmentEventTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DevelopmentEventTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.development_event_transition_model': 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'prepare_for_run': {
                'arguments': {
                    'dev_projects': 'dptm_results',
                    'model_configuration': 'model_configuration'
                    },
                'name': 'prepare_for_run',
                'output': '(all_project_types, all_project_units)'
                },
            'run': {
                'arguments': {
                    'debuglevel': 'debuglevel',
                    'projects': 'dptm_results',
                    'types': 'all_project_types',
                    'units': 'all_project_units',
                    'year': 'year'
                    },
                'output': 'development_events'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = DevelopmentEventTransitionModelConfigurationCreator(
            debuglevel = 9999,
            output_events = 'output_events',
            input_projects = 'input_projects',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.development_event_transition_model': 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'prepare_for_run': {
                'arguments': {
                    'dev_projects': 'input_projects',
                    'model_configuration': 'model_configuration'
                    },
                'name': 'prepare_for_run',
                'output': '(all_project_types, all_project_units)'
                },
            'run': {
                'arguments': {
                    'debuglevel': 9999,
                    'projects': 'input_projects',
                    'types': 'all_project_types',
                    'units': 'all_project_units',
                    'year': 'year'
                    },
                'output': 'output_events',
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()