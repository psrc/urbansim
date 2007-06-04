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


class HouseholdRelocationModelConfigurationCreator(HasStrictTraits):
    agent_set = Str('household')
    debuglevel = Trait('debuglevel', Str, Int)
    rate_table = Str('annual_relocation_rates_for_households')
    what = Str('households')
    
    output_index = Str('hrm_index')
    
    _model_name = 'household_relocation_model'
    
    def execute(self):
        # Names of intermediate objects used to get data between steps
        # in this model process.
        _resources = 'hrm_resources'
        
        return Configuration({
            'import': {
                'urbansim.models.%s_creator' % self._model_name: 'HouseholdRelocationModelCreator'
                },
            'init': {
                'arguments': {'debuglevel': self.debuglevel},
                'name': 'HouseholdRelocationModelCreator().get_model'
                },
            'prepare_for_run': {
                'arguments': {
                    'rate_storage': 'base_cache_storage',
                    'rate_table': "'%s'" % self.rate_table,
                    'what': "'%s'" % self.what,
                    },
                'name': 'prepare_for_run',
                'output': _resources,
                },
            'run': {
                'arguments': {
                    'agent_set': self.agent_set,
                    'resources': _resources,
                    },
                'output': self.output_index,
                }
            })
            

from opus_core.tests import opus_unittest 


class TestHouseholdRelocationModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = HouseholdRelocationModelConfigurationCreator()
        
        expected = Configuration({
            'import': {
                'urbansim.models.household_relocation_model_creator': 'HouseholdRelocationModelCreator'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel'},
                'name': 'HouseholdRelocationModelCreator().get_model'
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
        
    def test_with_arguments(self):
        creator = HouseholdRelocationModelConfigurationCreator(
            agent_set = 'agent_set',
            debuglevel = 9999,
            rate_table = 'rate_table',
            what = 'what',
            output_index = 'output_index',
            )
        
        expected = Configuration({
            'import': {
                'urbansim.models.household_relocation_model_creator': 'HouseholdRelocationModelCreator'
                },
            'init': {
                'arguments': {'debuglevel': 9999},
                'name': 'HouseholdRelocationModelCreator().get_model'
                },
            'prepare_for_run': {
                'arguments': {
                    'rate_storage': 'base_cache_storage',
                    'rate_table': "'rate_table'",
                    'what': "'what'"
                    },
                'name': 'prepare_for_run',
                'output': 'hrm_resources'
                },
            'run': {
                'arguments': {
                    'agent_set': 'agent_set',
                    'resources': 'hrm_resources'
                    },
                'output': 'output_index'
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
            
if __name__ == '__main__':
    opus_unittest.main()