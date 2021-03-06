# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    #"pda = (bayarea.parcel.pda_id).astype('i')",
    "schooldistrict = (parcel.schooldistrict_id)*(parcel.schooldistrict_id>0) + 99*(parcel.schooldistrict_id<1)",
    "neighborhood_type = (parcel.neighborhood_type + 1)*(parcel.neighborhood_type>-1)+ 6*(parcel.neighborhood_type<0)",
    "within_half_mile_transit = parcel.disaggregate(bayarea.node.transit_within_800_meters)",
    "parcel_acre = parcel.shape_area * 0.000247105381",
    "is_pda_id = (parcel.pda_id > 0).astype('i')" ,
    "is_pda_x_county = (parcel.county_id * (parcel.pda_id > 0)).astype('i')" ,
    "is_tpp  =  (parcel.tpp_id > 0).astype('i')",
    "region_id = 9*ones_like(parcel.parcel_id)",
	"is_open_space = ((parcel.aggregate(building.building_sqft)==0) + (safe_array_divide((0.000247105*parcel.shape_area),parcel.aggregate(0.000022956*building.building_sqft))>4))>0",

           ]
    
