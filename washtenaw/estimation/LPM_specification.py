# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

specification={
-2:
[
 ('constant', 'constant'),
#
 ('ln(urbansim.gridcell.total_residential_value_per_residential_unit_within_walking_distance)', 'LVU_RW'),
# ('urbansim.gridcell.gridcell_year_built', 'YRBLT'),
 ('urbansim.gridcell.is_outside_urban_growth_boundary', 'O_UGB'),
 ('urbansim.gridcell.is_near_arterial', 'ART'),
 ('urbansim.gridcell.is_near_highway', 'HWY'),
 ('urbansim.gridcell.ln_distance_to_highway', 'BLDHW'),
# ('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
# ('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
# ('urbansim.gridcell.is_in_wetland', 'BWET'),
#
 ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
#
# ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),
# ('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
 ('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
# ('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
# ('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
#
 ('urbansim.gridcell.ln_residential_units', 'BLDU'),
 ('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
#
# ('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
 ('urbansim.gridcell.ln_total_employment_within_walking_distance', 'LE_W'),
 ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
 ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
 ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#
# ('urbansim.gridcell.percent_commercial_within_walking_distance','PCW'),
# ('urbansim.gridcell.percent_industrial_within_walking_distance','PIW'), 
# ('urbansim.gridcell.percent_residential_within_walking_distance','PRW'),
# ('urbansim.gridcell.percent_developed_within_walking_distance', 'PDEVW'),
# ('urbansim.gridcell.percent_open_space_within_walking_distance','POSW'), 
 ('urbansim.gridcell.percent_water', 'PWATER'),
 ('urbansim.gridcell.percent_wetland', 'PWETLA'),
#
# ('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
# ('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
# ('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),
#
 ("urbansim.gridcell.ln_home_access_to_employment_1", "BLHAE1"), 
# ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),
# ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone', 'BWTH_DA'),
# ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk', 'BWTH_TW'), 
# ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_walk', 'BWTH_W'),
# ('psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_bike', 'BWTH_B'),
#
# ('psrc.gridcell.travel_time_hbw_am_drive_alone_to_cbd', 'TT_CBD'),
# ('psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone', 'WCH_DA'),

],
}
