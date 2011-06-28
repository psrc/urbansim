# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
    "skyharbor_enplanement_capacity = (building.other_spaces_name=='skyharbor_enplanement_capacity')*(building.other_spaces)",
    "williamsgateway_enplanement_capacity = (building.other_spaces_name=='williamsgateway_enplanement_capacity')*(building.other_spaces)",
    "hotel_motel_rooms = (building.other_spaces_name=='hotel_motel_rooms')*(building.other_spaces)",
    "is_developing_type = (building.building_type_id==1)+(building.building_type_id==2)+(building.building_type_id==3)+(building.building_type_id==4)+(building.building_type_id==5)",
    "bldg_sqft_constructed_this_year = (building.non_residential_sqft - building.non_residential_sqft_lag1)+((building.residential_units*building.sqft_per_unit)-(building.residential_units_lag1*building.sqft_per_unit))",
    "mpa_id = building.disaggregate(zone.mpa_id)",
    "is_building_type_rsf = urbansim_zone.building.is_building_type_rsf",
    "is_building_type_rmf = urbansim_zone.building.is_building_type_rmf",
    "is_building_type_retl = urbansim_zone.building.is_building_type_retl",
    "is_building_type_ind = urbansim_zone.building.is_building_type_ind",
    "is_building_type_off = urbansim_zone.building.is_building_type_off",
    "is_building_type_hot = urbansim_zone.building.is_building_type_hot",
    "occupied_hot_units_col = urbansim_zone.building.is_building_type_hot * (urbansim_zone.building.number_of_non_home_based_jobs * urbansim_zone.building.building_sqft_per_job)",
    "total_hot_units_col = urbansim_zone.building.is_building_type_hot * building.non_residential_sqft",
    "occupied_off_units_col = urbansim_zone.building.is_building_type_off * (urbansim_zone.building.number_of_non_home_based_jobs * urbansim_zone.building.building_sqft_per_job)",
    "total_off_units_col = urbansim_zone.building.is_building_type_off * building.non_residential_sqft",
    "occupied_ind_units_col = urbansim_zone.building.is_building_type_ind * (urbansim_zone.building.number_of_non_home_based_jobs * urbansim_zone.building.building_sqft_per_job)",
    "total_ind_units_col = urbansim_zone.building.is_building_type_ind * building.non_residential_sqft",
    "occupied_retl_units_col = urbansim_zone.building.is_building_type_retl * (urbansim_zone.building.number_of_non_home_based_jobs * urbansim_zone.building.building_sqft_per_job)",
    "total_retl_units_col = urbansim_zone.building.is_building_type_retl * building.non_residential_sqft",
    "occupied_rsf_units_col = urbansim_zone.building.is_building_type_rsf * urbansim_zone.building.number_of_households",
    "total_rsf_units_col = urbansim_zone.building.is_building_type_rsf * building.residential_units",
    "occupied_rmf_units_col = urbansim_zone.building.is_building_type_rmf * urbansim_zone.building.number_of_households",
    "total_rmf_units_col = urbansim_zone.building.is_building_type_rmf * building.residential_units",      

           ]

