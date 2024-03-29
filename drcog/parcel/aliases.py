# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "schooldistrict = (parcel.schooldistrict_id)*(parcel.schooldistrict_id>0) + 99*(parcel.schooldistrict_id<1)",
    "neighborhood_type = (parcel.neighborhood_type + 1)*(parcel.neighborhood_type>-1)+ 6*(parcel.neighborhood_type<0)",
    "within_half_mile_transit = parcel.dist_rail<2641",
    "parcel_acre = parcel.shape_area * 0.000247105381",
    "zone = parcel.zone_id",
    "parks = parcel.land_use_type_id==14"
           ]
