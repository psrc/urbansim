# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "zone_id = building.disaggregate(parcel.zone_id)",
    "county_id =  building.disaggregate(parcel.county_id)",
    "superdistrict_id = building.disaggregate(parcel.superdistrict_id)",
    "schooldistrict = building.disaggregate(parcel.school_district)",
    "neighborhood_type = building.disaggregate(bayarea.parcel.neighborhood_type)",
    "building_type = 1*(building.building_type_id==20) + 2*(building.building_type_id==2) + 2*(building.building_type_id==3) + 2*(building.building_type_id==11)",
    "jurisdiction_id = building.disaggregate(parcel.city_id)",
    "tenure_id = 1*(building.tenure<2) + 2*(building.tenure==2)",
    "building_type_id = building.building_type_id",
    "within_half_mile_transit = building.disaggregate(parcel.dist_rail< 2640)",
    "residential_building_type_id = 1*((building.residential_units>0)*(building.building_type_id==1)) + 2*((building.residential_units>0)*(building.building_type_id==2)) + 3*((building.residential_units>0)*(building.building_type_id==3))+ 4*((building.residential_units>0)*(building.building_type_id==4))+ 5*((building.residential_units>0)*(building.building_type_id>4))+ 6*(building.residential_units==0)",
           ]
