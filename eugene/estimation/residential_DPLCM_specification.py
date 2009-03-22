# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

#######
# In a command line, you can estimate using this command:
#  
# python urbansim/tools/start_estimation.py -c eugene.configs.baseline_estimation --model=residential_development_project_location_choice_model -s eugene.estimation.residential_DPLCM_specification
#
# see 
# python urbansim/tools/start_estimation.py --help
# for other options
#######

specification = {
    1:  # residential sub_model for 1 unit
        [
#
# ###   Economic Variables:
#
#        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
#        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
#        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
#
# ###   Developable Land Capacity:
#
#        ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
#        ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
#        ("urbansim.gridcell.is_on_steep_slope","SLOPE"),#
#        ("urbansim.gridcell.is_in_wetland","WTLND"),#
#        ("urbansim.gridcell.is_in_floodplain","FLOOD"),#
#        ("urbansim.gridcell.is_in_stream_buffer","STRBUF"),#
#        ("urbansim.gridcell.percent_open_space_within_walking_distance","POSW"),
#
# ###   Plan Types:  
#
#        ("urbansim.gridcell.is_plan_type_1","PT_1"),   #agriculture_rural_residential
#        ("urbansim.gridcell.is_plan_type_2","PT_2"),   #low_density_residential
#        ("urbansim.gridcell.is_plan_type_11","PT_11"),   #residential_high
#        ("urbansim.gridcell.is_plan_type_12","PT_12"),   #residential_light
#        ("urbansim.gridcell.is_plan_type_13","PT_13"),   #residential_low
#        ("urbansim.gridcell.is_plan_type_14","PT_14"),   #residential_medium
#        ("urbansim.gridcell.is_plan_type_15","PT_15"),   #residential_rural
#
# ###   Accessibility Variables:  
#  
#        ("urbansim.gridcell.is_near_arterial","ART"), #
#        ("urbansim.gridcell.is_near_highway","HWY"),
        ('urbansim.gridcell.travel_time_to_CBD', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#
        ],
    }