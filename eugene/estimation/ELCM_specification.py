# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
# 
######
# In a command line, you can estimate using these commands:
# Industrial: 
# python urbansim/tools/start_estimation.py -c eugene.configs.baseline_estimation --model=employment_location_choice_model --group=industrial -s eugene.estimation.ELCM_specification
#
# Commercial:
# python urbansim/tools/start_estimation.py -c eugene.configs.baseline_estimation --model=employment_location_choice_model --group=commercial -s eugene.estimation.ELCM_specification
#
# Home-based
# python urbansim/tools/start_estimation.py -c eugene.configs.baseline_estimation --model=employment_location_choice_model --group=home_based -s eugene.estimation.ELCM_specification
#
# see 
# python urbansim/tools/start_estimation.py --help
# for other options
#######

specification ={}

specification['industrial'] = { #industrial
1:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
2:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
3:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

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
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    #('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
4:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
5:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    #('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
6:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    #('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
7:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    #('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
}
specification['commercial'] = {  #commercial
1:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    #('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
2:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
        #: keep
    ('urbansim.gridcell.is_near_arterial', 'BART'),
        #:
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
        #: keep
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
        #: keep
    ('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
        #: keep
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
        #: keep
    ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

        #: keep
    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
        #: keep
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    #('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
        #: keep
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
3:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

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
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    #('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
4:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    ('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    #('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
5:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    ('urbansim.gridcell.is_near_arterial', 'BART'),
    ('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    ('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    #('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    #('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
    #('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

    #('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

    #('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    ('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
    #('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    #('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],
6:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
        #: keep
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
        #:
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

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
        #:
    #('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

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
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

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
    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),

    ],

8:
    [
    #('urbansim.gridcell.building_age', 'BAGE_BL'),
    #('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    #('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
    #('ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
    #('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW')

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

    ]
}

specification['home_based'] = { #home-based
-2:
    [
#     ('urbansim.gridcell.average_household_size', 'HHSIZE'),
#     ('urbansim.gridcell.average_income', 'AVG_INCOME'),
#     ('urbansim.gridcell.average_income_per_housing_unit', 'AVG_UNIT_INCOME'),

    #('urbansim.gridcell.building_age', 'BAGE_BL'),
#    ('urbansim.gridcell.is_near_arterial', 'BART'),
    #('urbansim.gridcell.is_near_highway', 'BHWY'),
    #('urbansim.gridcell.ln_distance_to_highway', 'BLDHIW'),
    #('urbansim.gridcell.is_in_floodplain', 'BFLOOD'),
    #('urbansim.gridcell.is_in_stream_buffer', 'BSTREAM'),
    #('urbansim.gridcell.is_in_wetland', 'BWET'),
    ('urbansim.gridcell.ln_total_land_value', 'BLTLV'),
    #('urbansim.gridcell.ln_average_land_value_per_acre_within_walking_distance', 'BLALVAW'),
#    ('urbansim.gridcell.ln_total_improvement_value', 'BLIMP'),
    #('ln(urbansim.gridcell.non_residential_improvement_value_per_sqft)', 'BLNIMPSQ'),
#    ('urbansim.gridcell.ln_total_value', 'BLTV'),

    #('urbansim.gridcell.ln_commercial_sqft', 'BLSFC'),
    #('urbansim.gridcell.ln_commercial_sqft_within_walking_distance', 'BLSFCW'),
    #('urbansim.gridcell.ln_industrial_sqft', 'BLSFI'),
    #('urbansim.gridcell.ln_industrial_sqft_within_walking_distance', 'BLSFIW'),
    #('urbansim.gridcell.ln_residential_units', 'BLDU'),
    #('urbansim.gridcell.ln_residential_units_within_walking_distance', 'BLDUW'),
#    ('urbansim.gridcell.ln_total_nonresidential_sqft_within_walking_distance', 'BLNRSFW'),

    ('urbansim.gridcell.percent_low_income_households_within_walking_distance', 'BPLIW'),
    ('urbansim.gridcell.percent_mid_income_households_within_walking_distance', 'BPMIW'),
#    ('urbansim.gridcell.percent_high_income_households_within_walking_distance', 'BPHIW'),

#    ('urbansim.gridcell.ln_work_access_to_employment_1', 'BLWAE_1'),
    ('urbansim.gridcell.ln_work_access_to_population_1', 'BLWAP_1'),

#    ('urbansim.gridcell.ln_total_population_within_walking_distance', 'BP_TW'),
    #('urbansim.gridcell.ln_total_employment_within_walking_distance', 'BE_TW'),

    #('urbansim.gridcell.ln_basic_sector_employment_within_walking_distance', 'BLE_BW'),
#    ('urbansim.gridcell.ln_retail_sector_employment_within_walking_distance', 'BLE_REW'),
    ('urbansim.gridcell.ln_service_sector_employment_within_walking_distance', 'BLE_SEW'),
#    ('urbansim.job_x_gridcell.ln_same_sector_employment_within_walking_distance', 'BLE_SAW'),
    #('urbansim.job_x_gridcell.same_sector_jobs_in_faz', 'BSECFAZ'),
    #('urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz', 'BLSECFAZ'),
    ('urbansim.gridcell.travel_time_to_CBD', "BTT_CBD"),

    ],
}
