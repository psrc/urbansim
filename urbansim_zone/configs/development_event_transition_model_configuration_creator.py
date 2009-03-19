# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import array

from opus_core.configuration import Configuration


class DevelopmentEventTransitionModelConfigurationCreator(object):
    _model_name = 'development_event_transition_model'
    
    def __init__(self,
        input_projects = 'dptm_results',
        output_events = 'development_events'):
        
        self.input_projects = input_projects
        self.output_events = output_events
    
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        
        return Configuration({
            'import': {
                'urbansim_zone.models.%s' % self._model_name: 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'run': {
                'arguments': {
                    'projects': self.input_projects,
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
                'urbansim_zone.models.development_event_transition_model': 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'run': {
                'arguments': {
                    'projects': 'dptm_results',
                    'year': 'year'
                    },
                'output': 'development_events'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = DevelopmentEventTransitionModelConfigurationCreator(
            output_events = 'output_events',
            input_projects = 'input_projects',
            )
        
        expected = Configuration({
            'import': {
                'urbansim_zone.models.development_event_transition_model': 'DevelopmentEventTransitionModel'
                },
            'init': {'name': 'DevelopmentEventTransitionModel'},
            'run': {
                'arguments': {
                    'projects': 'input_projects',
                    'year': 'year'
                    },
                'output': 'output_events',
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()
