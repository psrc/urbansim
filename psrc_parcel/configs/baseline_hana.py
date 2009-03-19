# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from baseline import Baseline

class BaselineHana(Baseline):

    multiple_runs=False
    multiple_runs_config = 'psrc_parcel.configs.multiple_runs_modification_hana'
    
    def __init__(self):
        config = Baseline()
        config['years'] = (2001, 2005)
        config['number_of_runs'] = 50
        config['seed'] = 1
        #config['cache_directory'] = '/Users/hana/urbansim_cache/psrc/parcel/relocation_models_estimation/cache_source_parcel'
        config['creating_baseyear_cache_configuration'].cache_directory_root = os.path.join(
                                                    config['creating_baseyear_cache_configuration'].cache_directory_root, '')
        #config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = '/Users/hana/urbansim_cache/psrc/parcel/relocation_models_estimation/cache_source_parcel'
        config['creating_baseyear_cache_configuration'].tables_to_cache = [
                    'households',
                    'buildings',
                    'parcels',
                    'gridcells',
                    'zones',
                    "jobs",
                    #"households_for_estimation",
                    #"households_for_estimation_LAG1",
                    #"jobs_for_estimation",
                    #"development_event_history",
                    "persons",
                    #"persons_for_estimation",
                    "travel_data",
                    "building_types",
                    "job_building_types",
                    'urbansim_constants',
                    "target_vacancies",
                    "non_home_based_employment_location_choice_model_coefficients",
                    "non_home_based_employment_location_choice_model_specification",
                    "household_location_choice_model_coefficients",
                    "household_location_choice_model_specification",
                    "household_relocation_choice_model_coefficients",
                    "household_relocation_choice_model_specification",
                    "workplace_relocation_choice_model_coefficients",
                    "workplace_relocation_choice_model_specification",
                    "real_estate_price_model_coefficients",
                    "real_estate_price_model_specification",
                    "annual_household_control_totals",
                    #"annual_relocation_rates_for_households",
                    "household_characteristics_for_ht",
                    "annual_employment_control_totals",
                    "annual_relocation_rates_for_jobs",
                    "land_use_types",
                    "generic_land_use_types",
                    'employment_sectors',
                    'employment_adhoc_sector_groups',
                    'employment_adhoc_sector_group_definitions',
                    'development_templates',
                    'development_template_components',
                    'development_constraints',
                    "building_sqft_per_job",
                    "fazes",
                    "large_areas",
                    "demolition_cost_per_sqft",
                    'constant_taz_columns',
                    #'zipcodes',
                    #'cities',
                    #'districts',
                    #'area_types',
                    "work_at_home_choice_model_coefficients",
                    "work_at_home_choice_model_specification",
                    "workplace_choice_model_for_resident_coefficients",
                    "workplace_choice_model_for_resident_specification",
                    "development_project_proposals",
                    "development_project_proposals_for_estimation",
                    #"school_districts",
                    #"tours",
                    ## some attribute coding lookup tables
                    #"education",
                    #"employment_status",
                    #"grade",
                    "race_names",
                    #"relationship",
                    #"sex",
                    #"student",
                    ]
        config['scenario_database_configuration'].database_name = 'psrc_activity2006_ver2_hana_est'
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
#                "modify_workers_jobs_after_moving_households",
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
                    'movers_ratio': 0.15,
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
                    'movers_ratio': 0.1,
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
                    'agent_set': 'person',
                    'agent_filter': "'urbansim_parcel.person.is_non_home_based_worker'",
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
                     'agent_filter': "'urbansim_parcel.person.is_non_home_based_worker_with_job'"
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
