# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configurations.household_transition_model_configuration_creator import HouseholdTransitionModelConfigurationCreator

class RegionalHouseholdTransitionModelConfigurationCreator(HouseholdTransitionModelConfigurationCreator):

    _model_name = 'regional_household_transition_model'
    
    def execute(self):
        conf = HouseholdTransitionModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalHouseholdTransitionModel'}
        conf['init']['name'] = 'RegionalHouseholdTransitionModel'
        conf['run']['output'] = 'regional_htm_index'
        return conf



from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestHouseholdTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalHouseholdTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'washtenaw.models.regional_household_transition_model': 'RegionalHouseholdTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel',
                              'location_id_name': "'grid_id'"},
                'name': 'RegionalHouseholdTransitionModel'
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
                    },
                'output': 'regional_htm_index'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
if __name__ == '__main__':
    opus_unittest.main()