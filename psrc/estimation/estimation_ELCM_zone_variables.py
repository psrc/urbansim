# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

specification ={}

specification['commercial'] = {  #commercial
1:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
#      ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
#    ('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    #('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
#    ('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 

 # ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
2:    
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
    ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
#    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 

 # ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
3:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
    ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
#    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),


#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
        
    ],
4:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
    ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
#    ('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),

#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
        
    ],
5:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
    ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),  
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
#    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
#    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),

#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
6:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz.', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),
    
 # ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
7:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),
    
#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
8:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
      ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    #('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),
    
    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
    
    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),
    
#    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    #('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    #('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),

#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
9:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
      ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),

#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
10:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
      ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #  ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    #('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
#    ('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),

#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
        
    ],
11:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
      ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('ln(urbansim.zone.residential_units)', 'BLDU'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),
    
#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
        
    ],
12:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
      ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),

#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
        
    ],
13:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
      ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    ('zone.aggregate(gridcell.industrial_sqft)', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),

    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    #('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),
    
    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
    
    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),
    
#    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    #('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    #('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),
    
#  ('LGCWPDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    
    ]
}

specification['industrial'] = { #industrial
1:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
#    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
    
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW'),

#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
2:    
    [
     #('urbansim.gridcell.building_age', 'BAGE_BL'),
      ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
#      ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #("urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #("urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #("urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #("urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #("urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')
    
#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
3:
    [
     #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    #('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
     ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')
    
#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
4:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')
    
#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
5:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    # ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')

#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
6:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
        ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
    #  ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
#      ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')

#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
7:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')
    
#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
8:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
        ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
#    ('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')

#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
9:
    [
     #('urbansim.gridcell.building_age', 'BAGE_BL'),
         ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
#    ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
#    ('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
#    ('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')

#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    
    ],
10:
    [
     #('urbansim.gridcell.building_age', 'BAGE_BL'),
         ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #  ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')

#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),    
    ],
11:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
       # ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
#      ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')

#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
    
    ],
12:
    [
     #('urbansim.gridcell.building_age', 'BAGE_BL'),
         ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
     # ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.job_x_gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')

#  ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(generalized_cost_weighted_access_to_population_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(generalized_cost_weighted_access_to_employment_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(generalized_cost_weighted_access_to_employment_hbw_am_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(employment_within_20_minutes_travel_time_hbw_am_walk = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
    ],
13:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
      #  ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),

    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
      #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    
    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
    #('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 
    
    #('urbansim.gridcell.travel_time_to_CBD', 'BTT_CBD'),
    #('urbansim.gridcell.trip_weighted_travel_time_from_zone_for_sov','WTTF_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_to_zone_for_sov','WTTT_SOV'),
    #('urbansim.gridcell.trip_weighted_travel_time_for_transit_walk','WTT_TW'),
    #('urbansim.gridcell.utility_for_SOV', 'UT_SOV'),
    #('urbansim.gridcell.utility_for_transit_walk', 'UT_TW')

 # ('ln(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone)','LGCWPDA'),
#  ('LGCWPTW = ln(generalized_cost_weighted_access_to_population_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

#  ('LNGCWEDA = ln(generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(generalized_cost_weighted_access_to_employment_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(generalized_cost_weighted_access_to_employment_hbw_am_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(employment_within_20_minutes_travel_time_hbw_am_walk = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
    
    ]
}


specification['home_based'] = {  #home-based
-2:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', 'BART'),
      ('zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    ('ln(urbansim.zone.average_land_value)', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),
    ('zone.aggregate(gridcell.commercial_sqft)', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    ('ln(urbansim.zone.residential_units)', 'BLDU'),  
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
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
    
    #('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', "BTT_129"),
    #('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_to_work_am_drive_alone', "BCTW_SOV"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_drive_alone', "BTWT_DA"),
#    ('psrc.gridcell.trip_weighted_average_time_hbw_to_work_am_transit_walk', "BTWT_TW"), 

#  ('LGCWPDA = ln(generalized_cost_weighted_access_to_population_hbw_am_drive_alone = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone))','LGCWPDA'),
#  ('LGCWPTW = ln(generalized_cost_weighted_access_to_population_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_transit_walk))','LGCWPTW'),  

  #('LNGCWEDA = ln(generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))','LNGCWEDA'),
#  ('LNGCWETW = ln(generalized_cost_weighted_access_to_employment_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))','LNGCWETW'),
#  ('LNGCWEW = ln(generalized_cost_weighted_access_to_employment_hbw_am_walk = gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_walk))','LNGCWEW'),
#  ('LNE20MDA = ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE20MDA'),
#  ('LNE20MTW = ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE20MTW'),
#  ('LNE20MW = ln(employment_within_20_minutes_travel_time_hbw_am_walk = gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))','LNE20MW'),

# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_129', 'TT_CBD'),
#  ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
    
    ],
}
