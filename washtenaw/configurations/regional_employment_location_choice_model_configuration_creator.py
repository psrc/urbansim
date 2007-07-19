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

from enthought.traits.api import Str
from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator as USELCMCC

class RegionalEmploymentLocationChoiceModelConfigurationCreator(USELCMCC):

    input_index = Str('regional_etm_index')
    _model_name = 'regional_employment_location_choice_model'
    
    def execute(self):
        conf = USELCMCC.execute(self)
        conf['import'] = {'washtenaw.models.%s' % self._model_name: 'RegionalEmploymentLocationChoiceModel'}
        conf['init']['name'] = 'RegionalEmploymentLocationChoiceModel'
        return conf

 
from opus_core.tests import opus_unittest 
from opus_core.configuration import Configuration

class TestEmploymentLocationChoiceModelConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = RegionalEmploymentLocationChoiceModelConfigurationCreator()
        
        expected = Configuration({
            'estimate': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_index': 'index',
                    'data_objects': 'datasets',
                    'debuglevel': 'debuglevel',
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                },
            'group_by_attribute': ('job_building_type', 'name'),
            'import': {
                'washtenaw.models.regional_employment_location_choice_model': 'RegionalEmploymentLocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'sampler': "'opus_core.samplers.weighted_sampler'",
                    'choices': "'urbansim.lottery_choices'",
                    'dataset_pool': 'dataset_pool',
                    'location_set': 'gridcell',
                    'sample_size_locations': 30,
                    'capacity_string': "'vacant_SSS_job_space'",
                    'estimation_weight_string': "'total_number_of_possible_SSS_jobs'",
                    'filter': None,
                    'estimation_size_agents': 1.,
                    'compute_capacity_flag': True,
                    'number_of_units_string': "'total_number_of_possible_SSS_jobs'",
                    'run_config': {'agent_units_string': None,
                                   'lottery_max_iterations': 3}
                    },
                'name': 'RegionalEmploymentLocationChoiceModel'
                },
            'prepare_for_estimate': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_for_estimation_storage': 'base_cache_storage',
                    'agents_for_estimation_table': "'jobs_for_estimation'",
                    'data_objects': 'datasets',
                    'portion_to_unplace': 1/12.,
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'employment_location_choice_model_specification'",
                    'filter': None
                    },
                'name': 'prepare_for_estimate',
                'output': '(specification, index)'
                },
            'prepare_for_run': {
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'employment_location_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'employment_location_choice_model_specification'"
                    },
                'name': 'prepare_for_run',
                'output': '(specification, coefficients)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'job',
                    'agents_index': 'regional_etm_index',
                    'chunk_specification': "{'records_per_chunk':50000}",
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