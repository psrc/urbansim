# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configs.hlcm_estimation_config import run_configuration as config

run_configuration = config.copy()
#run_configuration['models_configuration']['household_location_choice_model']["export_estimation_data"]=False
#run_configuration['models_configuration']['household_location_choice_model']["estimation_data_file_name"]="/tmp/HLCM_zone_estimate_data"

run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sample_size_locations'] = 30
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimate_config"]= \
                   {"weights_for_estimation_string":"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033",
                    "biogeme_model_name":"hlcm_parcel"}
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_set"] = "parcel"
#run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_id_string"] = "'household.parcel_id'"
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['submodel_string'] = "'psrc.household.number_of_nonhome_based_workers'"

run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["join_datasets"] = 'False'
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["filter"] = "'psrc.household.customized_filter'"
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["estimate"]["arguments"]['procedure']="'biogeme.mnl_estimation'"

run_configuration['creating_baseyear_cache_configuration'].tables_to_cache += [
#        'development_event_history',
        'edges',
        'parcels',
#        'gridcells',
#        'households',
#        'jobs',
#        'travel_data',
        'persons', #need to cache
#        'zones',
        'households_for_estimation'
        ]

run_configuration["datasets_to_preload"].merge({'zone':{}, 
                                                'household':{},
                                                'person':{"package_name":"psrc"},
                                                'parcel':{"package_name":"psrc"}
                                                })
run_configuration["models"] = [
#    {"household_relocation_model": ["run"]},
    {"household_location_choice_model": ["estimate"]}
]

if __name__ == '__main__':
    from .my_estimation_config import my_configuration
    from urbansim.estimation.estimator import Estimator
    from urbansim.estimation.estimator import update_controller_by_specification_from_module

    run_configuration = update_controller_by_specification_from_module(
                            run_configuration, "household_location_choice_model",
                            "inprocess.psrc_parcel.hlcm_parcel_specification")
    run_configuration.merge(my_configuration)
    estimator = Estimator(run_configuration, save_estimation_results=False)
    estimator.estimate()
#    estimator.reestimate("hlcm_parcel_specification")