# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration
from opus_core.misc import get_string_or_None

class EmploymentRelocationModelConfigurationCreator(object):
    
    _model_name = 'employment_transition_model'

    def __init__(self,
                debuglevel = 'debuglevel',
                agent_set = 'job',
                what = 'jobs',
                rate_table = 'annual_relocation_rates_for_jobs',
                location_id_name = 'grid_id',
                probabilities = 'urbansim.employment_relocation_probabilities',
                output_index = 'erm_index'):
        self.debuglevel = debuglevel
        self.agent_set = agent_set
        self.what = what
        self.rate_table = rate_table
        self.location_id_name = location_id_name
        self.probabilities = probabilities
        self.output_index = output_index
        
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _resources = 'erm_resources'
        
        return Configuration({
            'import': {
                'urbansim.models.employment_relocation_model_creator': 'EmploymentRelocationModelCreator'
                },
            'init': {
                'arguments': {
                              'debuglevel': self.debuglevel,
                              'location_id_name': "'%s'" % self.location_id_name,
                              'probabilities': get_string_or_None(self.probabilities),
                              },
                'name': 'EmploymentRelocationModelCreator().get_model'
                },
            'prepare_for_run': {
                'arguments': {
                    'rate_storage': 'base_cache_storage',
                    'rate_table': get_string_or_None(self.rate_table),
                    'what': "'%s'" % self.what,
                    },
                'name': 'prepare_for_run',
                'output': _resources,
                },
            'run': {
                'arguments': {
                    'resources': _resources, 
                    'agent_set': self.agent_set,
                    },
                'output': self.output_index,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestEmploymentRelocationModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = EmploymentRelocationModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.employment_relocation_model_creator': 'EmploymentRelocationModelCreator'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel',
                              'location_id_name': "'grid_id'",
                              'probabilities': "'urbansim.employment_relocation_probabilities'"},
                'name': 'EmploymentRelocationModelCreator().get_model',
                
                },
            'prepare_for_run': {
                'arguments': {
                    'rate_storage': 'base_cache_storage',
                    'rate_table': "'annual_relocation_rates_for_jobs'",
                    'what': "'jobs'"
                    },
                'name': 'prepare_for_run',
                'output': 'erm_resources'
                },
            'run': {
                'arguments': {
                    'resources': 'erm_resources', 
                    'agent_set': 'job'
                    },
                'output': 'erm_index'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = EmploymentRelocationModelConfigurationCreator(
            debuglevel = 9999,
            agent_set = 'agent_set',
            what = 'what',
            rate_table = 'rate_table',
            output_index = 'output_index',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.employment_relocation_model_creator': 'EmploymentRelocationModelCreator'
                },
            'init': {
                'arguments': {'debuglevel': 9999,
                              'location_id_name': "'grid_id'",
                              'probabilities': "'urbansim.employment_relocation_probabilities'",},
                'name': 'EmploymentRelocationModelCreator().get_model'
                },
            'prepare_for_run': {
                'arguments': {
                    'rate_storage': 'base_cache_storage',
                    'rate_table': "'rate_table'",
                    'what': "'what'"
                    },
                'name': 'prepare_for_run',
                'output': 'erm_resources'
                },
            'run': {
                'arguments': {
                    'resources': 'erm_resources', 
                    'agent_set': 'agent_set',
                    },
                'output': 'output_index',
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()