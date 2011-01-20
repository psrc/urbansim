# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configs.hlcm_estimation_config import HLCMEstimationConfig
from psrc_parcel.configs.baseline_estimation import BaselineEstimation
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
from my_estimation_config import my_configuration

#class HlcmParcelEstimation(BaselineEstimation): # comment this line out for urbansim.configs.hlcm_estimation_config
class HlcmParcelEstimationUrbansim(HLCMEstimationConfig): # comment this line out for psrc_parcel.configs.baseline_estimation
    def update_config(self):
        HLCMEstimationConfig.update_config(self) # comment this line out for psrc_parcel.configs.baseline_estimation
#        
        self.replace(my_configuration)
        estimate_config = {}
        estimate_config["export_estimation_data"]=False
        estimate_config["estimation_data_file_name"]="/tmp/HLCM_building_estimate_data"
        estimate_config["use_biogeme_data_format"]=True
#        estimate_config["weights_for_estimation_string"]=  "has_eg_1_units=building.residential_units>=1" #"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033"
        #"sampling_filter=(building.disaggregate(building_type.building_type_name)=='single_family_residential') + (building.disaggregate(building_type.building_type_name)=='multi_family_residential') + (building.disaggregate(building_type.building_type_name)=='condo_residential')"
        #"has_eg_1_units=urbansim.building.residential_units>=1"
            
        estimate_config["stratum"] = "psrc.parcel.is_in_city_seattle" #"psrc.parcel.stratify_by_is_in_city_seattle_and_is_single_family_unit"
        estimate_config["sample_size_from_each_stratum"] = 5
        estimate_config["sample_size_from_chosen_stratum"] = 4
        estimate_config["include_chosen_choice"] = True
        estimate_config['wesml_sampling_correction_variable'] = 'psrc_parcel.building.wesml_sampling_correction_variable'
        #estimate_config['submodel_string'] = "None"
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sample_size_locations'] = 30
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"#"'opus_core.samplers.stratified_sampler'"   #
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimate_config"] = estimate_config
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimation_weight_string"] = "'has_eg_1_units=building.residential_units>=1'"
                           #{"weights_for_estimation_string":"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033"}
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_set"] = "building"
        #self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_id_string"] = "'household.parcel_id'"
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['submodel_string'] = "'psrc.household.number_of_nonhome_based_workers'"
#        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['filter'] = None
        
        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["join_datasets"] = 'True'
        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'
        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["filter"] = None #"'psrc.household.customized_filter'"
        
        self["models"] = [
        #    {"household_relocation_model": ["run"]},
            {"household_location_choice_model": ["estimate"]}
        ]

class HlcmParcelEstimationPsrcParcel(BaselineEstimation): # comment this line out for urbansim.configs.hlcm_estimation_config
    def update_config(self):
#        HLCMEstimationConfig.update_config(self) # comment this line out for psrc_parcel.configs.baseline_estimation
#        
        self.replace(my_configuration)
        estimate_config = {}
        estimate_config["export_estimation_data"]=False
        estimate_config["estimation_data_file_name"]="/tmp/HLCM_building_estimate_data"
        estimate_config["use_biogeme_data_format"]=True
#        estimate_config["weights_for_estimation_string"]=  "has_eg_1_units=building.residential_units>=1" #"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033"
        #"sampling_filter=(building.disaggregate(building_type.building_type_name)=='single_family_residential') + (building.disaggregate(building_type.building_type_name)=='multi_family_residential') + (building.disaggregate(building_type.building_type_name)=='condo_residential')"
        #"has_eg_1_units=urbansim.building.residential_units>=1"
            
        estimate_config["stratum"] = "psrc.parcel.is_in_city_seattle" #"psrc.parcel.stratify_by_is_in_city_seattle_and_is_single_family_unit"
        estimate_config["sample_size_from_each_stratum"] = 5
        estimate_config["sample_size_from_chosen_stratum"] = 4
        estimate_config["include_chosen_choice"] = True
        estimate_config['wesml_sampling_correction_variable'] = 'psrc_parcel.building.wesml_sampling_correction_variable'
        #estimate_config['submodel_string'] = "None"
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sample_size_locations'] = 30
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"#"'opus_core.samplers.stratified_sampler'"   #
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimate_config"] = estimate_config
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["estimation_weight_string"] = "'has_eg_1_units=building.residential_units>=1'"
                           #{"weights_for_estimation_string":"psrc.parcel.residential_units_when_has_eg_1_surveyed_households_and_is_in_county_033"}
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_set"] = "building"
        #self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_id_string"] = "'household.parcel_id'"
        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['submodel_string'] = "'psrc.household.number_of_nonhome_based_workers'"
#        self["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['filter'] = None
        
        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["join_datasets"] = 'True'
        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'
        self["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["filter"] = None #"'psrc.household.customized_filter'"
        
        self["models"] = [
        #    {"household_relocation_model": ["run"]},
            {"household_location_choice_model": ["estimate"]}
        ]


from numpy import ndarray, allclose

def print_difference(dict1, dict2, key_sequence=[]):
    unique_keys = set(dict1.keys() + dict2.keys())
    for key in unique_keys:
        if not dict1.has_key(key):
            print "+the 1st dict: %s is missing" % "->".join(key_sequence + [key])
            continue

        if not dict2.has_key(key):
            print "-the 2nd dict: %s is missing" % "->".join(key_sequence + [key])
            continue
        
        try:
            dict1[key].keys()
            dict2[key].keys()
            is_dict = True
        except:
            is_dict = False
        
        if is_dict:
            print_difference(dict1[key], dict2[key], key_sequence + [key])
        else:
            is_different = True
            if type(dict1[key]) == ndarray:
                if type(dict2[key] == ndarray):
                    if allclose(dict1[key], dict2[key]):
                        is_different = False
                
            elif dict1[key] == dict2[key]:
                is_different  = False
            if is_different:
                print "+the 1st dict: %s=%s" % ("->".join(key_sequence + [key]), dict1[key])
                print "-the 2nd dict: %s=%s" % ("->".join(key_sequence + [key]), dict2[key] )
            
        pass
    
if __name__ == '__main__':
    urbansim_configuration = HlcmParcelEstimationUrbansim()
    urbansim_configuration.update_config()
    
    psrcparcel_configuration = HlcmParcelEstimationPsrcParcel()
    psrcparcel_configuration.update_config()
   
    print_difference(urbansim_configuration, psrcparcel_configuration)

