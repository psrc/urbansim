# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.configuration import Configuration
from opus_core.misc import get_string_or_None

class HouseholdRelocationModelConfigurationCreator(object):
    _model_name = 'household_relocation_model'
    
    def __init__(self,
                agent_set = 'household',
                debuglevel = 'debuglevel',
                rate_table = 'annual_relocation_rates_for_households',
                location_id_name = 'grid_id',
                probabilities = 'urbansim.household_relocation_probabilities',
                what = 'households',
                output_index = 'hrm_index'):
        self.agent_set = agent_set
        self.debuglevel = debuglevel
        self.rate_table = rate_table
        self.location_id_name = location_id_name
        self.probabilities = probabilities
        self.what = what
        self.output_index = output_index
        
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _resources = 'hrm_resources'
        
        return Configuration({
            'import': {
                'urbansim.models.%s_creator' % self._model_name: 'HouseholdRelocationModelCreator'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel,
                              'location_id_name': "'%s'" % self.location_id_name,
                              'probabilities': get_string_or_None(self.probabilities),
                                },
                'name': 'HouseholdRelocationModelCreator().get_model'
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
                    'agent_set': self.agent_set,
                    'resources': _resources,
                    },
                'output': self.output_index,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestHouseholdRelocationModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = HouseholdRelocationModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.household_relocation_model_creator': 'HouseholdRelocationModelCreator'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel',
                              'location_id_name': "'grid_id'",
                              'probabilities': "'urbansim.household_relocation_probabilities'"},
                'name': 'HouseholdRelocationModelCreator().get_model'
                },
            'prepare_for_run': {
                'arguments': {
                    'rate_storage': 'base_cache_storage',
                    'rate_table': "'annual_relocation_rates_for_households'",
                    'what': "'households'"
                    },
                'name': 'prepare_for_run',
                'output': 'hrm_resources'
                },
            'run': {
                'arguments': {
                    'agent_set': 'household',
                    'resources': 'hrm_resources'
                    },
                'output': 'hrm_index'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = HouseholdRelocationModelConfigurationCreator(
            agent_set = 'agent_set',
            debuglevel = 9999,
            rate_table = 'rate_table',
            what = 'what',
            output_index = 'output_index',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.household_relocation_model_creator': 'HouseholdRelocationModelCreator'
                },
            'init': {
                'arguments': {'debuglevel': 9999,
                              'location_id_name': "'grid_id'",
                              'probabilities': "'urbansim.household_relocation_probabilities'"                      
                                  },
                'name': 'HouseholdRelocationModelCreator().get_model'
                },
            'prepare_for_run': {
                'arguments': {
                    'rate_storage': 'base_cache_storage',
                    'rate_table': "'rate_table'",
                    'what': "'what'"
                    },
                'name': 'prepare_for_run',
                'output': 'hrm_resources'
                },
            'run': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'resources': 'hrm_resources'
                    },
                'output': 'output_index'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()