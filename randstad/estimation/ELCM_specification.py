# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

specification ={}
specification['commercial'] = {  #commercial
-2:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    ('urbansim.gridcell.ln_distance_to_highway', 'BLDHW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    ('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    ('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
#    ('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    #('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),
    
    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
    
    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),
    
    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    #('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    #('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 

    ],
}

specification['industrial'] = { #industrial
-2:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
#    ('urbansim.gridcell.is_near_arterial', 'BART'),
#    ('urbansim.gridcell.is_near_highway', 'BHWY'),
    ('urbansim.gridcell.ln_distance_to_highway', 'BLDHW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    ('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
#    ('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
#    ('urbansim.gridcell.ln_residential_units', 'BLDU'),
#    ('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
#    ('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
#    ('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),
    
    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
    
    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),
    
#    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
#    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    ('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')
    ],
}

specification['home_based'] = {  #home-based
-2:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    ('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    ('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    ('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    ('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('urbansim.gridcell.ln_residential_units', 'BLDU'),
    ('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    #('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
    ('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    ('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),
    
    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
    
    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),
    
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    ('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_to_CBD', "TT_CBD"),
    ],
}
