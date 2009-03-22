# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configs.hlcm_zone_estimation_config import run_configuration as config

run_configuration = config.copy()
run_configuration['models_configuration']['household_location_choice_model']["export_estimation_data"]=True
run_configuration['models_configuration']['household_location_choice_model']["estimation_data_file_name"]="/tmp/HLCM_zone_estimate_data"

run_configuration['creating_baseyear_cache_configuration'].tables_to_cache = run_configuration['creating_baseyear_cache_configuration'].tables_to_cache + ["parcels", "persons"]
run_configuration['datasets_to_preload']["person"] = {"package_name":"psrc"}
run_configuration['datasets_to_preload']["parcel"] = {"package_name":"psrc"}
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sample_size_locations']=None
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sampler']=None#"'opus_core.samplers.weighted_sampler'"
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['filter']= \
                                        "'psrc.zone.has_eg_1_households_with_1_nonhome_based_workers'"
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimate_config"]="models_configuration['household_location_choice_model']"
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["join_datasets"] = 'False'
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["filter"] = \
                                        "'psrc.household.has_1_nonhome_based_workers_and_valid_worker1_work_place_zone_id'"

run_configuration["models"] = [
#    {"household_relocation_model": ["run"]},
    {"household_location_choice_model": ["estimate"]}
]
