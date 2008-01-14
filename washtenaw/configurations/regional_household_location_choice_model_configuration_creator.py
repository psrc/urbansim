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

from urbansim.configurations.household_location_choice_model_configuration_creator import HouseholdLocationChoiceModelConfigurationCreator as USHLCMCC

class RegionalHouseholdLocationChoiceModelConfigurationCreator(USHLCMCC):
    
    _model_name = 'regional_household_location_choice_model'

    def __init__(self, 
                 input_index = 'hrm_index', 
                 lottery_max_iterations = 5, 
                 maximum_runs = 3, 
                 nchunks = 1,
                 records_per_chunk = 50000,
                 *args, **kwargs):
        USHLCMCC.__init__(self, 
                          input_index = input_index, 
                          lottery_max_iterations = lottery_max_iterations, 
                          maximum_runs = maximum_runs,
                          nchunks = nchunks,
                          *args, **kwargs)
        self.records_per_chunk = records_per_chunk
            
    def execute(self):
        conf = USHLCMCC.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalHouseholdLocationChoiceModel'}
        conf['init']['name'] = 'RegionalHouseholdLocationChoiceModel'
        conf['run']['arguments']['chunk_specification'] = "{'records_per_chunk':%s}" % self.records_per_chunk
        return conf

 
from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestHouseholdLocationChoiceModelConfiguration(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalHouseholdLocationChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_index': 'index',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'import': {
                'washtenaw.models.regional_household_location_choice_model': 'RegionalHouseholdLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'sampler': "'opus_core.samplers.weighted_sampler'",
                    'choices': "'urbansim.lottery_choices'",
                    'estimation': "'opus_core.bhhh_mnl_estimation'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'gridcell',
                    'sample_size_locations': 30,
                    'capacity_string': "'vacant_residential_units'",
                    'number_of_units_string': "'residential_units'",
                    'number_of_agents_string': "'number_of_households'",
                    'run_config': {'lottery_max_iterations': 5}
                    },
                'name': 'RegionalHouseholdLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'households_for_estimation'",
                    'data_objects': 'datasets',
                    'index_to_unplace': 'hrm_index',
                    'join_datasets': 'True',
                    'portion_to_unplace': 1/12.0,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'household_location_choice_model_specification'"
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'household_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'household_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_index': 'hrm_index',
                    'chunk_specification': "{'records_per_chunk':50000}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification',
                    'maximum_runs': 3
                    }
                }
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
                        
if __name__ == '__main__':
    opus_unittest.main()