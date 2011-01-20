# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration


class EventsCoordinatorConfigurationCreator(object):
    
    _model_name = 'events_coordinator'
    
    def __init__(self,
                location_set = 'gridcell',
                development_type_set = 'development_type',
                input_events = 'development_events',
                output_changed_indices = 'changed_indices',
                output_processed_development_event_indices = 'processed_development_event_indices'):
        self.location_set = location_set
        self.development_type_set = development_type_set
        self.input_events = input_events
        self.output_changed_indices = output_changed_indices
        self.output_processed_development_event_indices = output_processed_development_event_indices
        
    def execute(self):
        return Configuration({
            'import': {
                'urbansim.models.%s_and_storing' % self._model_name: 'EventsCoordinatorAndStoring'
                },
            'init': {'name': 'EventsCoordinatorAndStoring'},
            'run': {
                'arguments': {
                    'current_year': 'year',
                    'development_event_set': self.input_events,
                    'development_type_set': self.development_type_set,
                    'location_set': self.location_set,
                    'model_configuration': 'model_configuration'
                    },
                'output': '(%s, %s)' % (self.output_changed_indices, self.output_processed_development_event_indices)
                }
            })
            

from opus_core.tests import opus_unittest 


class TestEventsCoordinatorConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = EventsCoordinatorConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.events_coordinator_and_storing': 'EventsCoordinatorAndStoring'
                },
            'init': {'name': 'EventsCoordinatorAndStoring'},
            'run': {
                'arguments': {
                    'current_year': 'year',
                    'development_event_set': 'development_events',
                    'development_type_set': 'development_type',
                    'location_set': 'gridcell',
                    'model_configuration': 'model_configuration'
                    },
                'output': '(changed_indices, processed_development_event_indices)'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = EventsCoordinatorConfigurationCreator(
            location_set = 'location_set',
            development_type_set = 'development_type_set',
            input_events = 'input_events',
            output_changed_indices = 'output_changed_indices',
            output_processed_development_event_indices = 'output_processed_development_event_indices',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.events_coordinator_and_storing': 'EventsCoordinatorAndStoring'
                },
            'init': {'name': 'EventsCoordinatorAndStoring'},
            'run': {
                'arguments': {
                    'current_year': 'year',
                    'development_event_set': 'input_events',
                    'development_type_set': 'development_type_set',
                    'location_set': 'location_set',
                    'model_configuration': 'model_configuration'
                    },
                'output': '(output_changed_indices, output_processed_development_event_indices)'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()