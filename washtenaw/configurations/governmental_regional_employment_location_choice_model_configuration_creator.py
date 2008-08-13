#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

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