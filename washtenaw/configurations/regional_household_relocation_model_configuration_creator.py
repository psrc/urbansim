# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.configuration import Configuration
from urbansim.configurations.household_relocation_model_configuration_creator import HouseholdRelocationModelConfigurationCreator

class RegionalHouseholdRelocationModelConfigurationCreator(HouseholdRelocationModelConfigurationCreator):
    
    _model_name = 'regional_agent_relocation_model'
    
    def execute(self):
        conf = HouseholdRelocationModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalAgentRelocationModel'}
        conf['init']['name'] = 'RegionalAgentRelocationModel'
        conf['init']['arguments']['model_name'] = "'Regional Household Relocation Model'"
        return conf
 

from opus_core.tests import opus_unittest 


class TestRegionalHouseholdRelocationModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalHouseholdRelocationModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'washtenaw.models.regional_agent_relocation_model': 'RegionalAgentRelocationModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel',
                              'location_id_name': "'grid_id'",
                              'probabilities': "'urbansim.household_relocation_probabilities'",
                              'model_name': "'Regional Household Relocation Model'"},
                'name': 'RegionalAgentRelocationModel'
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
                   
            
if __name__ == '__main__':
    opus_unittest.main()