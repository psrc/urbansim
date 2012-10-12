# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "zone_id = building.disaggregate(parcel.zone_id)",
    "county_id =  building.disaggregate(parcel.county_id)",
    "superdistrict_id = building.disaggregate(parcel.superdistrict_id)",
    "schooldistrict = building.disaggregate(bayarea.parcel.schooldistrict)",
    "neighborhood_type = building.disaggregate(bayarea.parcel.neighborhood_type)",
    "building_type = 1*(building.building_type_id<2) + 2*(building.building_type_id==2) + 3*(building.building_type_id>2)",
    "jurisdiction_id = building.disaggregate(parcel.jurisdiction_id)",
    "building_type_id = building.building_type_id",
    "within_half_mile_transit = building.disaggregate(bayarea.parcel.within_half_mile_transit)",
    "building_sqft_per_employee=building.disaggregate(employment_submarket.building_sqft_per_employee)",
    "total_job_spaces = safe_array_divide(bayarea.building.non_residential_sqft, bayarea.building.building_sqft_per_employee)",
    "vacant_job_spaces = clip_to_zero(bayarea.building.total_job_spaces - bayarea.building.employees)",
    "establishments=building.number_of_agents(establishment)",
    "employees=building.aggregate(establishment.employees)",
    "tenure_id = 1*(building.tenure==1) + 2*(building.tenure==2) + 3*(building.tenure==-1)",
           ]
