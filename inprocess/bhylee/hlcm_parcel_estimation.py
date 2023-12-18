# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configs.hlcm_estimation_config import HLCMEstimationConfig
from psrc_parcel.configs.baseline_estimation import BaselineEstimation
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
from .my_estimation_config import my_configuration

class HlcmParcelEstimation(BaselineEstimation): # comment out for urbansim.configs.hlcm_estimation_config
#class HlcmParcelEstimation(HLCMEstimationConfig): # comment out for psrc_parcel.configs.baseline_estimation
    def update_config(self):
#        HLCMEstimationConfig.update_config(self) # comment out for psrc_parcel.configs.baseline_estimation
#        
        self.replace(my_configuration)
        estimate_config = {}
#        estimate_config["export_estimation_data"]=True
#        estimate_config["estimation_data_file_name"]="/tmp/HLCM_building_estimate_data"
#        estimate_config["use_biogeme_data_format"]=True
#        estimate_config["weights_for_estimation_string"]=  "has_eg_1_units=building.residential_units>=1" #"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033"
        #"sampling_filter=(building.disaggregate(building_type.building_type_name)=='single_family_residential') + (building.disaggregate(building_type.building_type_name)=='multi_family_residential') + (building.disaggregate(building_type.building_type_name)=='condo_residential')"
        #"has_eg_1_units=urbansim.building.residential_units>=1"
            
#        estimate_config["stratum"] = "psrc.parcel.is_in_city_seattle" #"psrc.parcel.stratify_by_is_in_city_seattle_and_is_single_family_unit"
#        estimate_config["sample_size_from_each_stratum"] = 5
#        estimate_config["sample_size_from_chosen_stratum"] = 4
#        estimate_config["include_chosen_choice"] = True
        estimate_config['wesml_sampling_correction_variable'] = 'psrc_parcel.building.wesml_sampling_correction_variable'
        #estimate_config['submodel_string'] = "None"
#        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sample_size_locations'] = 30
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"#"'opus_core.samplers.stratified_sampler'"   #
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimate_config"] = estimate_config
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimation_weight_string"] = "'has_eg_1_units=building.residential_units>=1'" 
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["capacity_string"] = "'has_eg_1_units=building.residential_units>=1'"
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["number_of_agents_string"] = "'(building.building_id < 0).astype(int32)'"
        
#        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimation_weight_string"] = "'urbansim_parcel.building.vacant_residential_units'"
#        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimation_weight_string"] = "'psrc_parcel.building.residential_units'"
                           #{"weights_for_estimation_string":"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033"}
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_set"] = "building"
        #self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_id_string"] = "'household.parcel_id'"
#        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['submodel_string'] = "'psrc.household.number_of_nonhome_based_workers'"

        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["variable_package"]="'urbansim_parcel'"

        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["join_datasets"] = 'True'
        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'
        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["filter"] = "'household.move == 1'"#None #"'psrc.household.customized_filter'"
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['filter'] = "'urbansim_parcel.building.is_residential'"
#        self["datasets_to_preload"].merge({"tour":{}, "person":{}})
#        self["datasets_to_cache_after_each_model"] += ["person"]
        self["models"] = [
#            {"household_relocation_model": ["run"]},
#            {"tour_schedule_model": ["run"]},
            {"household_location_choice_model": ["estimate"]}
        ]

if __name__ == '__main__':
    from .my_estimation_config import my_configuration
    from urbansim.estimation.estimator import Estimator
    from urbansim.estimation.estimator import update_controller_by_specification_from_module
    from opus_core.simulation_state import SimulationState
    from opus_core.store.attribute_cache import AttributeCache

    run_configuration = HlcmParcelEstimation()
    run_configuration.update_config()
    run_configuration = update_controller_by_specification_from_module(
                            run_configuration, "household_location_choice_model",
                            "inprocess.bhylee.hlcm_parcel_specification")
    er = Estimator(run_configuration, save_estimation_results=False)
    
    er.estimate()
#    er.create_prediction_success_table()
#    er.create_prediction_success_table(choice_geography_id="area_type_id=building.disaggregate(zone.area_type_id, intermediates=[parcel])" )
#    er.create_prediction_success_table(choice_geography_id="building_type_id=building.building_type_id" )
#    er.create_prediction_success_table(choice_geography_id="large_area_id=building.disaggregate(faz.large_area_id, intermediates=[zone, parcel])" )
#    er.reestimate("hlcm_parcel_specification")