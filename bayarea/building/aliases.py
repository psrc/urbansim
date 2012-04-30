# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "zone_id = building.disaggregate(parcel.zone_id)",
    "superdistrict_id = building.disaggregate((parcel.superdistrict_id)*(parcel.superdistrict_id>0)+(parcel.superdistrict_id<1))",
    "schooldistrict = building.disaggregate((parcel.schooldistrict_id)*(parcel.schooldistrict_id>0) + 99*(parcel.schooldistrict_id<1))",
    "neighborhood_type = building.disaggregate((parcel.neighborhood_type + 1)*(parcel.neighborhood_type>-1)+ 6*(parcel.neighborhood_type<0))",
    "building_type = 1*(building.building_type_id<2) + 2*(building.building_type_id==2) + 3*(building.building_type_id>2)",
    "jurisdiction_id = building.disaggregate(parcel.jurisdiction_id)",
    "tenure_id = 1*(building.tenure<2) + 2*(building.tenure==2)",
    "building_type_id = building.building_type_id",
    "within_half_mile_transit = building.disaggregate(bayarea.node.transit_within_800_meters,intermediates=[parcel])"
           ]
#"building_type = 1*(building.building_type_id==1) + 2*(building.building_type_id==2) + 3*(building.building_type_id>2)"