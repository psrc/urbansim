#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from urbansim.configurations.development_project_location_choice_model_configuration_creator import DevelopmentProjectLocationChoiceModelConfigurationCreator as USDPLCMCC

class RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator(USDPLCMCC):
     
    records_per_chunk = Int(1000)
    def execute(self):
        conf = USDPLCMCC.execute(self)
        conf['import'] = {'washtenaw.models.regional_development_project_location_choice_model': 
                              'RegionalDevelopmentProjectLocationChoiceModel'}
        conf['init']['name'] = 'RegionalDevelopmentProjectLocationChoiceModel'
        return conf


from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestDevelopmentProjectLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator(
            project_type = 'project_type',
            )
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'projects',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'washtenaw.models.regional_development_project_location_choice_model': 'RegionalDevelopmentProjectLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'location_set': 'gridcell',
                    'model_configuration': "model_configuration['development_project_types']['project_type']",
                    'project_type': "'project_type'",
                    'submodel_string': "'size_category'"
                    },
                'name': 'RegionalDevelopmentProjectLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'base_year': "resources['base_year']",
                    'categories': "model_configuration['development_project_types']['project_type']['categories']",
                    'events_for_estimation_storage': 'base_cache_storage',
                    'events_for_estimation_table': "'development_event_history'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'project_type_development_location_choice_model_specification'",
                    'urbansim_constant': 'urbansim_constant'
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, projects)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'project_type_development_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'project_type_development_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': "dptm_results['project_type']",
                    'chunk_specification': "{'records_per_chunk':300}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
                    
if __name__ == '__main__':
    opus_unittest.main()