# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration


class HouseholdTransitionModelConfigurationCreator(object):
    _model_name = 'household_transition_model'
    
    def __init__(self,
                 debuglevel = 'debuglevel',
                 household_set = 'household',
                 location_id_name = 'grid_id'):
        self.debuglevel = debuglevel
        self.household_set = household_set
        self.location_id_name = location_id_name
        
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _characteristics = 'characteristics'
        _control_totals = 'control_totals'
        
        return Configuration({
            'import': {
                'urbansim.models.%s' % self._model_name: 'HouseholdTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel,
                              'location_id_name': "'%s'" % self.location_id_name},
                'name': 'HouseholdTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': '(%s, %s)' % (_control_totals, _characteristics)
                },
            'run': {
                'arguments': {
                    'characteristics': _characteristics,
                    'control_totals': _control_totals,
                    'household_set': self.household_set,
                    'year': 'year'
                    }
                }
            })
            

from opus_core.tests import opus_unittest 


class TestHouseholdTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = HouseholdTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.household_transition_model': 'HouseholdTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel',
                              'location_id_name': "'grid_id'"},
                'name': 'HouseholdTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': '(control_totals, characteristics)'
                },
            'run': {
                'arguments': {
                    'characteristics': 'characteristics',
                    'control_totals': 'control_totals',
                    'household_set': 'household',
                    'year': 'year'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = HouseholdTransitionModelConfigurationCreator(
            debuglevel = 9999,
            household_set = 'household_set',
            location_id_name='zone_id'
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.household_transition_model': 'HouseholdTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 9999,
                              'location_id_name': "'zone_id'"},
                'name': 'HouseholdTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': '(control_totals, characteristics)'
                },
            'run': {
                'arguments': {
                    'characteristics': 'characteristics',
                    'control_totals': 'control_totals',
                    'household_set': 'household_set',
                    'year': 'year'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()