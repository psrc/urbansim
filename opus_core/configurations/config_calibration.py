# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

calibration_paris = {
    'xml_config' : '/home/atschirhar/opus/project_configs/paris_zone.xml',
    'scenario' : 'paris_zone_calibration2',
    'calib_datasets' : {'establishment_location_choice_model_coefficients': 'estimate'},
    'subset' : None,
    'subset_patterns' : {'establishment_location_choice_model_coefficients':['coefficient_name', '_celcm$']},
    'target_expression' : "zgpgroup.aggregate((establishment.employment)*(establishment.disappeared==0),intermediates=[building,zone,zgp])",
    'target_file' : '/workspace/opus/data/paris_zone/temp_data/zgpgroup_totemp00.csv',
    'skip_cache_cleanup': True
}
    
calibration_bayarea_developer = {
    'xml_config' : '/workspace/opus/project_configs/bay_area_parcel_unit_price.xml',
    'scenario' : 'developer_calibration',
    'calib_datasets' : {'cost_shifter': 'residential_shifter'},
    'subset' : None,
    'subset_patterns' : None,
    'target_expression' : "county.aggregate(building.residential_units,intermediates=[parcel]",
    'target_file' : '/workspace/opus/data/bay_area_parcel/calibration_targets/county_resunits2011.csv'}
