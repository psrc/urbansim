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

from enthought.traits.api import HasStrictTraits, Str, Int, Float, Trait

from opus_core.configuration import Configuration


class HouseholdTransitionModelConfigurationCreator(HasStrictTraits):
    debuglevel = Trait('debuglevel', Str, Int)
    household_set = Str('household')
    
    _model_name = 'household_transition_model'
    
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
                'arguments': {'debuglevel': self.debuglevel},
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
                'arguments': {'debuglevel': 'debuglevel'},
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
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.household_transition_model': 'HouseholdTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 9999},
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