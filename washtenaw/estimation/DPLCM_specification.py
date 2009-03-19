# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

specification = {}
#
# ############################# Residential ##############################  
#
specification['residential'] = {
    1:  # residential sub_model for 1 unit
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
        ("urbansim.gridcell.has_1_units","UNIT_1"),#
        ("urbansim.gridcell.has_2_units","UNIT_2"),#
        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
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
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
#        "urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
#
# ###   Developable Land Capacity:
#
#        ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
#        ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#
    2:  # residential sub_model for 2 units
        [
#
# ###   Economic Variables:
#
#        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
        ("urbansim.gridcell.has_2_units","UNIT_2"),#
        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"), #
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
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
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
# 
    3:  # residential sub_model for 3 units
        [
#
# ###   Economic Variables:
#
#        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"), #
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
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
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
# 
    4:  # residential sub_model for 4 and 5 units
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
#        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"), #
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
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
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#
    5:  # residential sub_model for 6 to 10 units
        [
#
# ###   Economic Variables:
#
#        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#         ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
#        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"), #
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
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
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#
    6:  # residential sub_model for 11 to 20 units
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#         ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
#        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"), #
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
#
# ###   Developable Land Capacity:
#
#        ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
#        ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#
    7:  # residential sub_model for more than 20 units
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#         ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
#        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
#        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"), #
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
#
# ###   Developable Land Capacity:
#
        ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
#        ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#
    }
#
# ############################# Industrial ##############################  
#
specification['industrial'] = { #industrial
#   
    1:  # industrial sub_model for 5,000 sqft or less
        [
#
# ###   Economic Variables:
#
#        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
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
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#   
    2:  # industrial sub_model for >5,000 sqft and <= 10,000 sqft
        [
#
# ###   Economic Variables:
#
#        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
#        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
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
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#   
    3:  # industrial sub_model for >10,000 sqft and <= 20,000 sqft
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
#        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
#
# ###   Developable Land Capacity:
#
#        ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
#        ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#   
    4:  # industrial sub_model for >20,000 sqft and <= 40,000 sqft
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
#        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
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
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#   
    5:  # industrial sub_model for >40,000 sqft
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
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
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
# 
    }
#
# ############################# Commercial ##############################  
#
specification['commercial'] = { #commercial
#   
    1:  # commercial sub_model for 1000 sqft or less
        [
#
# ###   Economic Variables:
#
#        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
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
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
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
        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
# 
    2:  # commercial sub_model for >1,000 sqft and <=2,000 sqft
        [
#
# ###   Economic Variables:
#
#        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
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
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
#        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
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
        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#   
    3:  # commercial sub_model for >2,000 sqft and <=5,000 sqft
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
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
#        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
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
        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
#        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#   
    4:  # commercial sub_model for >5,000 sqft and <=10,000 sqft
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
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
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
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
        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#   
    5:  # commercial sub_model for >10,000 commercial sqft
        [
#
# ###   Economic Variables:
#
        ("urbansim.gridcell.ln_total_value","LV"), #variable name, coefficient name
#        ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),         
#        ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),         
#        ("urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance","LALVAW"),#
#        ("urbansim.gridcell.ln_average_residential_value_per_housing_unit_within_walking_distance","LARVUW"),
#
# ###   Population Variables:
#
        ("urbansim.gridcell.ln_total_population_within_walking_distance","LP_W"),
#
# ###   Residential/Housing Units Variables:
#        
#        ("urbansim.gridcell.ln_residential_units","LDU"),
#        ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#        ("urbansim.gridcell.ln_residential_units_within_walking_distance","LDUW"),
#        ("urbansim.gridcell.has_0_units","UNIT_0"),#
#        ("urbansim.gridcell.has_1_units","UNIT_1"),#
#        ("urbansim.gridcell.has_2_units","UNIT_2"),#
#        ("urbansim.gridcell.has_3_to_5_units","UNIT_35"),#
#
# ###   Employment Variables:
#    
#        ("urbansim.gridcell.ln_total_employment_within_walking_distance" ,"LE_W"),
#        ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#        ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#        ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ###   Non-residential Land Variables:
#
#        ("urbansim.gridcell.ln_commercial_sqft","LSFC"),
#        ("urbansim.gridcell.has_0_commercial_sqft","SFC_0"),#
#        ("urbansim.gridcell.ln_commercial_sqft_within_walking_distance","LSFCW"),#
#        ("urbansim.gridcell.ln_industrial_sqft","LSFI"), #
#        ("urbansim.gridcell.has_0_industrial_sqft","SFI_0"),#
        ("urbansim.gridcell.ln_industrial_sqft_within_walking_distance","LSFIW"),#
#        ("urbansim.gridcell.percent_commercial_within_walking_distance","PCW"),
#        ("urbansim.gridcell.percent_industrial_within_walking_distance","PIW"), 
#
# ###   General (Residential and Non-residential) Land Development Variables:
#
        ("urbansim.gridcell.percent_developed_within_walking_distance","PDEVW"),#
#        ("urbansim.gridcell.n_recent_transitions_to_developed_within_walking_distance", "RDV"),
#
# ###   Developable Land Capacity:
#
#        ("urbansim.gridcell.ln_developable_residential_units_capacity","LDEVRU"),         
#        ("urbansim.gridcell.ln_developable_residential_units_capacity_within_walking_distance","LDEVRUW"),         
#        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity","LDEVSFC"),
        ("urbansim.gridcell.ln_developable_commercial_sqft_capacity_within_walking_distance","LDEVSFCW"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity","LDEVSFI"),
#        ("urbansim.gridcell.ln_developable_industrial_sqft_capacity_within_walking_distance","LDEVSFIW"),  
#
# ###   Environment/Policy Variables:
#
#        ("urbansim.gridcell.is_outside_urban_growth_boundary","O_UGB"),  
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
        ("urbansim.gridcell.is_near_arterial","ART"), #
#        ("urbansim.gridcell.is_near_highway","HWY"),  #
#        ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#
#        ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
        ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', "WTH_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', "WTH_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', "WTH_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', "WTH_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),
#
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "WTW_DA"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "WTW_TW"), 
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_walk', "WTW_W"),
#        ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_bike', "WTW_B"),
#        ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', 'WCW_DA'),
#
        ],
#   
    }