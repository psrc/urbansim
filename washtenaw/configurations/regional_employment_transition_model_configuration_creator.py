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

from urbansim.configurations.employment_transition_model_configuration_creator import EmploymentTransitionModelConfigurationCreator

class RegionalEmploymentTransitionModelConfigurationCreator(EmploymentTransitionModelConfigurationCreator):
 
    _model_name = 'regional_employment_transition_model'
    
    def execute(self):
        conf = EmploymentTransitionModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalEmploymentTransitionModel'}
        conf['init']['name'] = 'RegionalEmploymentTransitionModel'
        conf['run']['output'] = 'regional_etm_index'
        return conf


from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestEmploymentTransitionModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalEmploymentTransitionModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'washtenaw.models.regional_employment_transition_model': 'RegionalEmploymentTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel', 'location_id_name': "'grid_id'"},
                'name': 'RegionalEmploymentTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': 'control_totals'
                },
            'run': {
                'arguments': {
                    'control_totals': 'control_totals',
                    'job_building_types': 'job_building_type',
                    'job_set': 'job',
                    'year': 'year'
                    },
                'output': 'regional_etm_index'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
if __name__ == '__main__':
    opus_unittest.main()