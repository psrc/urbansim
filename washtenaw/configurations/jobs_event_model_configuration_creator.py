# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration


class JobsEventModelConfigurationCreator(object):

    _model_name = 'agent_event_model'

    def __init__(self,
                location_set = 'gridcell',
                agent_set = 'job',
                agent_event_set = 'jobs_event'):
        self.location_set = location_set
        self.agent_event_set = agent_event_set
        self.agent_set = agent_set
            
    def execute(self):        
        return Configuration({
            'import': {
                'washtenaw.models.%s' % self._model_name: 'AgentEventModel'
                },
            'init': {'name': 'AgentEventModel'},
            'run': {
                'arguments': {
                    'location_set': self.location_set,
                    'agent_event_set': self.agent_event_set,
                    'agent_set':self.agent_set,
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
        creator = JobsEventModelConfigurationCreator()
        
        expected = Configuration({
           'import': {
                'washtenaw.models.agent_event_model': 'AgentEventModel'
                },
            'init': {'name': 'AgentEventModel'},
            'run': {
                'arguments': {
                    'location_set': 'gridcell',
                    'agent_event_set': 'jobs_event',
                    'agent_set':'job',
                    'current_year': 'year',
                    'dataset_pool': 'dataset_pool'
                    }
                }
            })
        result = creator.execute()
        self.assertDictsEqual(result, expected)           
            
if __name__ == '__main__':
    opus_unittest.main()
