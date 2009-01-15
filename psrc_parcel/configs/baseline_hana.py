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

from baseline import Baseline

class BaselineHana(Baseline):

    multiple_runs=True
    multiple_runs_config = 'psrc_parcel.configs.multiple_runs_modification_hana'
    
    def __init__(self):
        config = Baseline()
        config['years'] = (2001, 2001)
        config['number_of_runs'] = 10
        config['seed'] = 1
        #config['creating_baseyear_cache_configuration'].cache_directory = '/Users/hana/urbansim_cache/psrc/cache_source_parcel'
        config['cache_directory'] = '/Users/hana/urbansim_cache/psrc/parcel/relocation_models_estimation/cache_source_parcel'
        config['creating_baseyear_cache_configuration'].cache_directory_root = '/Users/hana/urbansim_cache/psrc/parcel'
        config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = '/Users/hana/urbansim_cache/psrc/cache_source_parcel'
        #config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = '/Users/hana/urbansim_cache/psrc/parcel/relocation_models_estimation/cache_source_parcel'
        config['scenario_database_configuration'].database_name = 'psrc_activity2006_ver2_hana'
        config['models'] = [ # models are executed in the same order as in this list
                "real_estate_price_model",
                "expected_sale_price_model",
                "development_proposal_choice_model",
                "building_construction_model",
                "modify_workers_jobs_after_moving_households", # from demolished buildings
                "modify_workers_jobs_after_moving_jobs", # from demolished buildings
                "household_transition_model",
                "employment_transition_model",
                'job_person_consistency_keeper',
                "household_relocation_choice_model",
                "household_location_choice_model",
                "modify_workers_jobs_after_moving_households",
                "employment_relocation_model",
                {"employment_location_choice_model":{'group_members': ['non_home_based']}},
                'distribute_unplaced_jobs_model',
                'distribute_unplaced_mining_utilities_jobs_model',
                "modify_workers_jobs_after_moving_jobs",
                'work_at_home_choice_model',
                'workplace_relocation_choice_model',
                'workplace_choice_model_for_resident'
                ]
        config['models_configuration']['household_relocation_choice_model'] = {}
        config['models_configuration']['household_relocation_choice_model']['controller'] = {
            'import': {
                'urbansim.models.agent_relocation_choice_model': 'AgentRelocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'location_id_name': "'building_id'",
                    'choice_attribute_name': "'move'",
                    'dataset_pool': 'dataset_pool'
                    },
                'name': 'AgentRelocationChoiceModel'
                },
            'prepare_for_run': {
                "name": "prepare_for_run",
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'household_relocation_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'household_relocation_choice_model_specification'",
                    'agent_set': 'household'
                    },
                'output': '(specification, coefficients, _index)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_index' : '_index',
                    'chunk_specification': "{'nchunks':1}",
                    'coefficients': 'coefficients',
                    'specification': 'specification'
                    },
                'output': 'hrm_index'
                },                
             "prepare_for_estimate": {
                 "name": "prepare_for_estimate",                                      
                 "arguments": {
                     "agent_set":"household",
                     },
                 "output": "(specification, agents_index)"
                 },
            'estimate': {
                'arguments': {
                    'agent_set': 'household',
                    'agents_index': 'agents_index',
                    'procedure': "'opus_core.bhhh_mnl_estimation'",
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                 },
            }
        config['models_configuration']['workplace_relocation_choice_model'] = {}
        config['models_configuration']['workplace_relocation_choice_model']['controller'] = {
            'import': {
                'urbansim.models.agent_relocation_choice_model': 'AgentRelocationChoiceModel'
                },
            'init': {
                'arguments': {
                    'location_id_name': "'job_id'",
                    'choice_attribute_name': "'changed_job'",
                    'dataset_pool': 'dataset_pool'
                    },
                'name': 'AgentRelocationChoiceModel'
                },
            'prepare_for_run': {
                "name": "prepare_for_run",
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'workplace_relocation_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'workplace_relocation_choice_model_specification'",
                    'agent_set': 'person'
                    },
                'output': '(specification, coefficients, _index)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'person',
                    'agents_index' : '_index',
                    'chunk_specification': "{'nchunks':1}",
                    'coefficients': 'coefficients',
                    'specification': 'specification'
                    },
                'output': 'person_index'
                },                
             "prepare_for_estimate": {
                 "name": "prepare_for_estimate",                                      
                 "arguments": {
                     "agent_set":"person",
                     },
                 "output": "(specification, agents_index)"
                 },
            'estimate': {
                'arguments': {
                    'agent_set': 'person',
                    'agents_index': 'agents_index',
                    'procedure': "'opus_core.bhhh_mnl_estimation'",
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                 },
            }
        config['models_configuration']['workplace_choice_model_for_resident']['controller']['run']['arguments']['agents_index'] = 'person_index'
        self.merge(config)
        if self.multiple_runs:
            self.sample_inputs()
            
if __name__ == "__main__":
    config = BaselineHana()
