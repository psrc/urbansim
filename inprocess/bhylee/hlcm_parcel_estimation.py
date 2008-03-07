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

from urbansim.configs.hlcm_estimation_config import run_configuration as config
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
#
estimate_config = {}
estimate_config["export_estimation_data"]=False
estimate_config["estimation_data_file_name"]="/tmp/HLCM_parcel_estimate_data"
estimate_config["use_biogeme_data_format"]=True
estimate_config["weights_for_estimation_string"]=  "has_eg_1_units=parcel.residential_units>=1" #"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033"
#"sampling_filter=(building.disaggregate(building_type.building_type_name)=='single_family_residential') + (building.disaggregate(building_type.building_type_name)=='multi_family_residential') + (building.disaggregate(building_type.building_type_name)=='condo_residential')"
#"has_eg_1_units=urbansim.building.residential_units>=1"
    
estimate_config["stratum"] = "psrc.parcel.is_in_city_seattle" #"psrc.parcel.stratify_by_is_in_city_seattle_and_is_single_family_unit"
estimate_config["sample_size_from_each_stratum"] = 5
estimate_config["sample_size_from_chosen_stratum"] = 4
estimate_config["include_chosen_choice"] = True
#estimate_config['submodel_string'] = "None"

run_configuration = config.copy()
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sample_size_locations'] = 30
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"#"'opus_core.samplers.stratified_sampler'"   #
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimate_config"]= \
                    estimate_config
                   #{"weights_for_estimation_string":"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033"}
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_set"] = "parcel"
#run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_id_string"] = "'household.parcel_id'"
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['submodel_string'] = "'psrc.household.number_of_nonhome_based_workers'"

run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["join_datasets"] = 'False'
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["filter"] = None #"'psrc.household.customized_filter'"

run_configuration["models"] = [
#    {"household_relocation_model": ["run"]},
    {"household_location_choice_model": ["estimate"]}
]

if __name__ == '__main__':
    from my_estimation_config import my_configuration
    from urbansim.estimation.estimator import Estimator
    from urbansim.estimation.estimator import update_controller_by_specification_from_module
    from opus_core.simulation_state import SimulationState
    from opus_core.store.attribute_cache import AttributeCache
    
    SimulationState().set_cache_directory(my_configuration['cache_directory']) 
    SessionConfiguration(
        new_instance = True,
        package_order = ['psrc','urbansim','opus_core'],
        package_order_exceptions = {},
        in_storage = AttributeCache()) 


    #SessionConfiguration(new_instance=True,
                         #package_order=['psrc','urbansim','opus_core'],
                         #package_order_exceptions={},                              
                         #in_storage=AttributeCache())

    run_configuration = update_controller_by_specification_from_module(
                            run_configuration, "household_location_choice_model",
                            "inprocess.psrc_parcel.hlcm_parcel_specification")
    run_configuration.replace(my_configuration)
    estimator = Estimator(run_configuration, save_estimation_results=False)
    estimator.estimate()
#    estimator.reestimate("hlcm_parcel_specification")