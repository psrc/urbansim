# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configurations.governmental_employment_location_choice_model_configuration_creator import GovernmentalEmploymentLocationChoiceModelConfigurationCreator
from opus_core.configuration import Configuration


class GovernmentalRegionalEmploymentLocationChoiceModelConfigurationCreator(GovernmentalEmploymentLocationChoiceModelConfigurationCreator):

    def execute(self):  
        conf = GovernmentalEmploymentLocationChoiceModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.regional_scaling_jobs_model': 'RegionalScalingJobsModel'}
        conf['init']['name'] = 'RegionalScalingJobsModel'
        return conf

from opus_core.tests import opus_unittest 


class TestGovernmentalEmploymentLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = GovernmentalRegionalEmploymentLocationChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'import': {'washtenaw.models.regional_scaling_jobs_model': 'RegionalScalingJobsModel'},
            'init': {
                'arguments': {'debuglevel': 'debuglevel',
                              'filter': None,
                              'dataset_pool': 'dataset_pool'},
                'name': 'RegionalScalingJobsModel'
                },
            'run': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_index': 'erm_index',
                    'data_objects': 'datasets',
                    'location_set': 'gridcell',
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        

if __name__ == '__main__':
    opus_unittest.main()