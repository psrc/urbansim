# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
       "sf_buildings = (parcel.aggregate(building.building_type_id<3)).astype(float32)",
       "sf_capacity = (safe_array_divide(parcel.parcel_sqft,parcel.disaggregate(zoning.min_lot_size))).astype(float32)",
       "remaining_sf_capacity = (honolulu_parcel.parcel.sf_capacity - honolulu_parcel.parcel.sf_buildings).astype(float32)",
           ]