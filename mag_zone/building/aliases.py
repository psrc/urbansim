# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
    "skyharbor_enplanement_capacity = (building.other_spaces_name=='skyharbor_enplanement_capacity')*(building.other_spaces)",
    "williamsgateway_enplanement_capacity = (building.other_spaces_name=='williamsgateway_enplanement_capacity')*(building.other_spaces)",
    "hotel_motel_rooms = (building.other_spaces_name=='hotel_motel_rooms')*(building.other_spaces)",
    "is_developing_type = (building.building_type_id==1)+(building.building_type_id==2)+(building.building_type_id==3)+(building.building_type_id==4)+(building.building_type_id==6)+(building.building_type_id==7)+(building.building_type_id==8)+(building.building_type_id==9)+(building.building_type_id==10)",
    "bldg_sqft_constructed_this_year = (building.non_residential_sqft - building.non_residential_sqft_lag1)+((building.residential_units*building.sqft_per_unit)-(building.residential_units_lag1*building.sqft_per_unit))",
    "mpa_id = building.disaggregate(zone.mpa_id)",
    "is_residential = building.disaggregate(building_type.is_residential)",
    "tazi03_id = building.disaggregate(zone.tazi03_id)",
    "raz2012_id = building.disaggregate(zone.raz2012_id)",
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
    "num_of_pub_jobs = building.aggregate(job.sector_id == 21)",
    "num_of_pub_local_jobs = building.aggregate(job.sector_id == 22)",
    "is_building_type_pub = (building.building_type_id == 14)",
    "is_building_type_pub_local = (building.building_type_id == 16)",
    "weight_for_pub_local_jobs = mag_zone.building.num_of_pub_local_jobs + (numpy.logical_and(building.building_type_id == 16, mag_zone.building.num_of_pub_local_jobs == 0)*(building.non_residential_sqft/50)).astype(int32)",
    "wah_capacity = numpy.minimum(building.aggregate(household.workers), 3*building.number_of_agents(household)) - building.aggregate(job.home_based_status == 1)",
    "mpa_population = building.disaggregate(zone.disaggregate(mpa.aggregate(household.persons)))",
    "mpa_city_jobs = building.disaggregate(mpa.aggregate(mag_zone.building.num_of_pub_jobs))",
    "vacant_residential_units_with_negatives = building.residential_units - urbansim_zone.building.number_of_households",
    "vacant_non_home_based_job_spaces_with_negatives = urbansim_zone.building.total_non_home_based_job_spaces - urbansim_zone.building.number_of_non_home_based_jobs",
    "vacant_home_based_job_spaces_with_negatives = urbansim_zone.building.total_home_based_job_spaces - urbansim_zone.building.number_of_home_based_jobs",
    "number_of_non_seasonal_household = building.aggregate(household.is_seasonal == 0)",
    "total_non_home_based_job_spaces = numpy.round(safe_array_divide(building.non_residential_sqft, urbansim_zone.building.building_sqft_per_job))",
    "total_home_based_job_spaces = numpy.minimum(building.aggregate(household.workers), 3)",     
    "vacant_non_home_based_job_spaces = clip_to_zero(mag_zone.building.total_non_home_based_job_spaces - urbansim_zone.building.number_of_non_home_based_jobs)",
#    "vacant_home_based_job_spaces = clip_to_zero(mag_zone.building.total_home_based_job_spaces - urbansim_zone.building.number_of_home_based_jobs)",
    "vacant_home_based_job_spaces = clip_to_zero(mag_zone.building.wah_capacity)",      
           ]

