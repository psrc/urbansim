# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .base_configuration import AbstractUrbansimConfiguration

class tables_to_cache(object):
    def get_tables_to_cache(self):
        return ['annual_employment_control_totals',
                    'annual_household_control_totals',
                    'buildings',
                    'building_types',
                    'development_event_history',
                    'gridcells',
                    'households',
                    'job_building_types',
                    'jobs',
                    'travel_data',
                    'zones',
                    'counties',
                    'commercial_employment_location_choice_model_coefficients',
                    'commercial_employment_location_choice_model_specification',
                    'home_based_employment_location_choice_model_specification',
                    'home_based_employment_location_choice_model_coefficients',
                    'industrial_employment_location_choice_model_coefficients',
                    'industrial_employment_location_choice_model_specification',
                    'industrial_building_location_choice_model_coefficients',
                    'industrial_building_location_choice_model_specification',
                    'residential_building_location_choice_model_coefficients',
                    'residential_building_location_choice_model_specification',
                    'commercial_building_location_choice_model_coefficients',
                    'commercial_building_location_choice_model_specification',
                    'real_estate_price_model_coefficients',
                    'real_estate_price_model_specification',
                    'fazes',
                    'urbansim_constants',
                    'household_location_choice_model_coefficients',
                    'household_location_choice_model_specification',
                    'plan_type_group_definitions',
                    'plan_type_groups',
                    'large_areas',
                    'household_characteristics_for_ht',
                    'development_types',
                    'development_type_group_definitions',
                    'development_constraints',
                    'annual_relocation_rates_for_households',
                    'annual_relocation_rates_for_jobs',
                    'base_year',
                    'cities',
                    'development_events',
                    'development_type_groups',
                    'employment_adhoc_sector_group_definitions',
                    'employment_adhoc_sector_groups',
                    'employment_sectors',
                    'plan_types',
                    'race_names',
                    'target_vacancies',
                    'jobs_for_estimation',
                    "households_for_estimation",
                    "development_events_exogenous",
                    "job_building_types"
                    ]

run_configuration = AbstractUrbansimConfiguration()

run_configuration['datasets_to_cache_after_each_model'] =[ # datasets to be cached after each model,
        'household',
        'job',
        'building',
        'zone']

run_configuration['datasets_to_preload']['building_type'] = {}
run_configuration['datasets_to_preload']['building'] = {}

run_configuration['models'] = [ # models are executed in the same order as in this list
        "real_estate_price_model",
        'building_transition_model',
        'building_relocation_model',
        {'building_location_choice_model': {'group_members': ['residential', 'commercial', 'industrial']}},
         "household_transition_model",
        "employment_transition_model",
        "household_relocation_model",
        "household_location_choice_model",
        "employment_relocation_model",
        {"employment_location_choice_model": {"group_members": "_all_"}},
        "distribute_unplaced_jobs_model",
        ]

run_configuration['models_in_year'] = \
     {run_configuration['years'][0]: ["prepare_datasets_for_aggregation", "flush_datasets",
        'building_transition_model',
        'building_relocation_model',
        {'building_location_choice_model': {'group_members': ['residential', 'commercial', 'industrial']}},
         "household_transition_model",
        "employment_transition_model",
        "household_relocation_model",
        "household_location_choice_model",
        "employment_relocation_model",
        {"employment_location_choice_model": {"group_members": "_all_"}},
        "distribute_unplaced_jobs_model",
        ]
}

_controller_configuration = {}

for model in list(run_configuration['models_configuration'].keys()):
    if 'controller' in run_configuration['models_configuration'][model]:
        _controller_configuration[model] = run_configuration['models_configuration'][model]['controller']

_controller_configuration["prepare_datasets_for_aggregation"] = {
    "import": {"urbansim.models.prepare_datasets_for_aggregation":
                    "PrepareDatasetsForAggregation"},
    "init": {
        "name": "PrepareDatasetsForAggregation"},
     "run": {
        "arguments": {"datasets_variables": "{household: ['urbansim.household.zone_id'], " + \
                                             "job: ['urbansim.job.zone_id'], " + \
                                             "building: ['urbansim.building.zone_id'], " + \
                                             "zone: ['total_maximum_development_residential = zone.aggregate(urbansim.gridcell.total_maximum_development_residential)', " + \
                                              "'total_maximum_development_commercial = zone.aggregate(urbansim.gridcell.total_maximum_development_commercial)', " + \
                                              "'total_maximum_development_industrial = zone.aggregate(urbansim.gridcell.total_maximum_development_industrial)', " + \
                                              "'developable_minimum_residential_units = zone.aggregate(urbansim.gridcell.developable_minimum_residential_units)', " + \
                                              "'developable_minimum_commercial_sqft = zone.aggregate(urbansim.gridcell.developable_minimum_commercial_sqft)', " + \
                                              "'developable_minimum_industrial_sqft = zone.aggregate(urbansim.gridcell.developable_minimum_industrial_sqft)', " + \
                                              "'is_near_arterial = zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', " + \
                                              "'is_near_highway = zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', " + \
                                              "'acres_of_land = zone.aggregate(urbansim.gridcell.acres_of_land)', " + \
                                              "'urbansim.zone.industrial_sqft_per_job', " + \
                                              "'urbansim.zone.commercial_sqft_per_job', " + \
                                              "'urbansim.zone.number_of_gridcells', " + \
                                              "'urbansim.zone.vacant_land_sqft', ]" + \
                                              "}",
                      "data_objects": "datasets"
                      },
        }
    }

_controller_configuration["flush_datasets"] = {
    "import": {"urbansim.models.flush_datasets":
                    "FlushDatasets"},
    "init": {
        "name": "FlushDatasets"},
     "run": {
        "arguments": {"datasets": '[gridcell]'}
             }
  }

_controller_configuration["real_estate_price_model"]["run"]["arguments"]["dataset"] = "zone"
_controller_configuration["real_estate_price_model"]["estimate"]["arguments"]["dataset"] = "zone"
_controller_configuration["real_estate_price_model"]["prepare_for_estimate"]["arguments"]["dataset"] = "zone"
_controller_configuration["building_transition_model"]["run"]["arguments"]["location_set"] = "zone"
_controller_configuration["building_relocation_model"]["init"]["arguments"]["location_id_name"] = "'zone_id'"
_controller_configuration["building_location_choice_model"]["init"]["arguments"]["location_set"] = "zone"
_controller_configuration["building_location_choice_model"]["prepare_for_run"] = {
                    "name": "prepare_for_run",
                    "arguments": {"specification_storage": "base_cache_storage",
                                  "specification_table": "'building_location_choice_model_specification'",
                                  "coefficients_storage": "base_cache_storage",
                                  "coefficients_table": "'building_location_choice_model_coefficients'",
                                 },
                    "output": "(specification, coefficients)"
                    }
_controller_configuration["building_location_choice_model"]["run"]["arguments"]["chunk_specification"] = "{'records_per_chunk':10000}"
_controller_configuration["building_location_choice_model"]["prepare_for_estimate"]["arguments"]["location_id_variable"] = \
                                                                                                    "'urbansim.building.zone_id'"
_controller_configuration["household_relocation_model"]["init"]["arguments"]["location_id_name"] = "'zone_id'"
_controller_configuration["household_location_choice_model"]["init"]["arguments"]["location_set"] = "zone"
_controller_configuration["household_location_choice_model"]["init"]["arguments"]["demand_string"] = "'zone.residential_demand'"
_controller_configuration["household_location_choice_model"]["init"]["arguments"]["run_config"] = \
                            "{'number_of_units_string': 'buildings_residential_units', 'capacity_string': 'vacant_residential_units_from_buildings'}"
_controller_configuration["household_location_choice_model"]["init"]["arguments"]["estimate_config"] = \
                            "{'weights_for_estimation_string': 'buildings_residential_units'}"
_controller_configuration["household_location_choice_model"]["run"]["arguments"]["chunk_specification"] = "{'records_per_chunk':100000}"
_controller_configuration["household_location_choice_model"]["prepare_for_estimate"]["arguments"]["location_id_variable"] = \
                                                                                                    "'urbansim.household.zone_id'"
_controller_configuration["household_location_choice_model"]["prepare_for_estimate"]["arguments"] = {
                              "specification_storage": "base_cache_storage",
                              "specification_table": "'household_location_choice_model_specification'",
                              "agent_set": "household",
                              "agents_for_estimation_storage": "base_cache_storage",
                              "agents_for_estimation_table": "'households_for_estimation'",
                              "join_datasets": "True",
                              "location_id_variable": "'urbansim.household.zone_id'",
                              "index_to_unplace":  None,
                              "compute_lambda": True,
                              "grouping_location_set": "faz",
                              "movers_variable": "'urbansim.zone.number_of_potential_household_movers'",
                              "movers_index": "hrm_index",
                              "data_objects": "datasets"
                                  }

_controller_configuration["employment_relocation_model"]["init"]["arguments"]["location_id_name"] = "'zone_id'"
model_name = "employment_location_choice_model"
_controller_configuration[model_name]["init"]["arguments"]["location_set"] = "zone"
_controller_configuration[model_name]["init"]["arguments"]["estimation_weight_string"] = "'annual_estimated_SSS_job_supply'"
_controller_configuration[model_name]["init"]["arguments"]["demand_string"] = "'zone.SSS_demand'"
_controller_configuration[model_name]["init"]["arguments"]["capacity_string"] = "'vacant_SSS_job_space_from_buildings'"
_controller_configuration[model_name]["run"]["arguments"]["chunk_specification"] = "{'records_per_chunk':100000}"
_controller_configuration[model_name]["prepare_for_estimate"]["arguments"] = {
                                "specification_storage": "base_cache_storage",
                                "specification_table": "'employment_location_choice_model_specification'",
                                "agent_set": "job",
                                "agents_for_estimation_storage": "base_cache_storage",
                                "agents_for_estimation_table": "'jobs_for_estimation'",
                                "join_datasets": "False",
                                "location_id_variable": "'urbansim.job.zone_id'",
                                "index_to_unplace":  None,
                                "compute_lambda": True,
                                "grouping_location_set": "faz",
                                "movers_variable": "'urbansim.zone.number_of_potential_SSS_job_movers'",
                                "movers_index": "erm_index",
                                "data_objects": "datasets"
                            }

model_name = "home_based_employment_location_choice_model"
_controller_configuration[model_name] = run_configuration['models_configuration'][model_name]['controller']
_controller_configuration[model_name]["init"]["arguments"]["location_set"] = "zone"
_controller_configuration[model_name]["init"]["arguments"]["capacity_string"] = "'vacant_SSS_job_space'"
_controller_configuration[model_name]["init"]["arguments"]["estimation_weight_string"] = "'annual_estimated_SSS_job_supply'"
_controller_configuration[model_name]["init"]["arguments"]["number_of_units_string"] = "'buildings_residential_units'"
_controller_configuration[model_name]["prepare_for_estimate"]["arguments"] = \
    _controller_configuration["employment_location_choice_model"]["prepare_for_estimate"]["arguments"]

model_name = "governmental_employment_location_choice_model"
_controller_configuration[model_name] = run_configuration['models_configuration'][model_name]['controller']
_controller_configuration[model_name]["run"]["arguments"]["location_set"] = "zone"

_controller_configuration["distribute_unplaced_jobs_model"]["run"]["arguments"]["location_set"] = "zone"

for model in list(_controller_configuration.keys()):
    if model not in list(run_configuration["models_configuration"].keys()):
        run_configuration["models_configuration"][model] = {}
    run_configuration["models_configuration"][model]["controller"] = _controller_configuration[model]

from opus_core.configuration import Configuration
run_configuration = Configuration(run_configuration)