# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator

class RegionalEmploymentRelocationModelConfigurationCreator(EmploymentRelocationModelConfigurationCreator):
    
    _model_name = 'regional_agent_relocation_model'
    
    def execute(self):
        conf = EmploymentRelocationModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalAgentRelocationModel'}
        conf['init']['name'] = 'RegionalAgentRelocationModel'
        conf['init']['arguments']['model_name'] = "'Regional Employment Relocation Model'"
        return conf
 

from opus_core.tests import opus_unittest 


class TestRegionalHouseholdRelocationModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
 
    def test_defaults(self):
        creator = RegionalEmploymentRelocationModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'washtenaw.models.regional_agent_relocation_model': 'RegionalAgentRelocationModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel',
                              'location_id_name': "'grid_id'",
                              'probabilities': "'urbansim.employment_relocation_probabilities'",
                              'model_name': "'Regional Employment Relocation Model'"},
                'name': 'RegionalAgentRelocationModel',
                
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
                   
            
if __name__ == '__main__':
    opus_unittest.main()