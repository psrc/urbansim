# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "zone_id = building.disaggregate(parcel.zone_id)",
    "county_id =  building.disaggregate(parcel.county_id)",
    "superdistrict_id = building.disaggregate(parcel.superdistrict_id)",
    "schooldistrict = building.disaggregate(parcel.school_district)",
    "neighborhood_type = building.disaggregate(bayarea.parcel.neighborhood_type)",
    "building_type = 1*(building.building_type_id==20) + 2*(building.building_type_id==24) + 3*(building.building_type_id==2) + 4*(building.building_type_id==3)",
    "emp_building_type = (building.building_type_id==0) + (building.building_type_id)",
    "jurisdiction_id = building.disaggregate(parcel.city_id)",
    "tenure_id = 1*(building.tenure<2) + 2*(building.tenure==2)",
    "building_type_id = building.building_type_id",
    "within_half_mile_transit = building.disaggregate(parcel.dist_rail< 2640)",
    "residential_building_type_id = 1*((building.residential_units>0)*(building.building_type_id==20)) + 2*((building.residential_units>0)*(building.building_type_id==24)) + 3*((building.residential_units>0)*(building.building_type_id==2))+ 4*((building.residential_units>0)*(building.building_type_id==3))+ 5*(building.residential_units==0)",
    "number_of_non_home_based_jobs = building.aggregate((establishment.home_based_status==0)*(establishment.employees))",
    "occupied_spaces=urbansim_parcel.building.is_residential * urbansim_parcel.building.number_of_households + numpy.logical_not(urbansim_parcel.building.is_residential) * drcog.building.number_of_non_home_based_jobs *urbansim_parcel.building.building_sqft_per_job",
    "total_spaces=urbansim_parcel.building.is_residential * building.residential_units + numpy.logical_not(urbansim_parcel.building.is_residential) * building.non_residential_sqft",
    "total_job_spaces = safe_array_divide(building.non_residential_sqft, drcog.building.building_sqft_per_employee)",
    "vacant_job_spaces = clip_to_zero(drcog.building.total_job_spaces - drcog.building.employees)",
    "employees=building.aggregate(establishment.employees)",
    "building_sqft_per_employee=urbansim_parcel.building.building_sqft_per_job",
           ]
