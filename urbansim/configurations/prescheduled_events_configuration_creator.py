# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.configuration import Configuration


class PrescheduledEventsConfigurationCreator(object):
    _model_name = 'prescheduled_events'
    
    def __init__(self,
                 output_events = 'development_events'):
        self.output_events = output_events
        
    def execute(self):
        return Configuration({
            'import': {
                'urbansim.models.process_prescheduled_development_events': 'ProcessPrescheduledDevelopmentEvents'
                },
            'init': {'name': 'ProcessPrescheduledDevelopmentEvents'},
            'run': {
                'arguments': {'storage': 'base_cache_storage'},
                'output': self.output_events,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestPrescheduledEventsConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = PrescheduledEventsConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.process_prescheduled_development_events': 'ProcessPrescheduledDevelopmentEvents'
                },
            'init': {'name': 'ProcessPrescheduledDevelopmentEvents'},
            'run': {
                'arguments': {'storage': 'base_cache_storage'},
                'output': 'development_events'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = PrescheduledEventsConfigurationCreator(
            output_events = 'output_events',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.process_prescheduled_development_events': 'ProcessPrescheduledDevelopmentEvents'
                },
            'init': {'name': 'ProcessPrescheduledDevelopmentEvents'},
            'run': {
                'arguments': {'storage': 'base_cache_storage'},
                'output': 'output_events'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()