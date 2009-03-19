# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.configuration import Configuration


class DeletionEventModelConfigurationCreator(object):

    
    _model_name = 'deletion_event_model'
    
    def __init__(self,
                location_set = 'gridcell',
                deletion_event_set = 'deletion_event'):
        self.location_set = location_set
        self.deletion_event_set = deletion_event_set
        
    def execute(self):        
        return Configuration({
            'import': {
                'washtenaw.models.%s' % self._model_name: 'DeletionEventModel'
                },
            'init': {'name': 'DeletionEventModel'},
            'run': {
                'arguments': {
                    'location_set': self.location_set,
                    'deletion_event_set': self.deletion_event_set,
                    'current_year': 'year',
                    'dataset_pool': 'dataset_pool'
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestDeletionEventModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = DeletionEventModelConfigurationCreator()
        
        expected = Configuration({
           'import': {
                'washtenaw.models.deletion_event_model': 'DeletionEventModel'
                },
            'init': {'name': 'DeletionEventModel'},
            'run': {
                'arguments': {
                    'location_set': 'gridcell',
                    'deletion_event_set': 'deletion_event',
                    'current_year': 'year',
                    'dataset_pool': 'dataset_pool'
                    }
                }
            })
        result = creator.execute()
        self.assertDictsEqual(result, expected)           
            
if __name__ == '__main__':
    opus_unittest.main()