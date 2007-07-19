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

from urbansim.configurations.household_transition_model_configuration_creator import HouseholdTransitionModelConfigurationCreator

class RegionalHouseholdTransitionModelConfigurationCreator(HouseholdTransitionModelConfigurationCreator):

    _model_name = 'regional_household_transition_model'
    
    def execute(self):
        conf = HouseholdTransitionModelConfigurationCreator.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalHouseholdTransitionModel'}
        conf['init']['name'] = 'RegionalHouseholdTransitionModel'
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
                'arguments': {'debuglevel': 'debuglevel'},
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
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
if __name__ == '__main__':
    opus_unittest.main()