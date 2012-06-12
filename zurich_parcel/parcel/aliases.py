# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
       "building_sqft_per_unit = safe_array_divide(parcel.building_sqft, parcel.residential_units)",
       "building_sqft = parcel.aggregate(building.building_sqft)",
       "lot_sqft_per_unit = safe_array_divide(parcel.lot_sf, parcel.residential_units)",
       "residential_units = parcel.aggregate(building.residential_units)",
       "remaining_non_residential_sqft_capacity = parcel.non_residential_sqft_capacity - parcel.aggregate(building.non_residential_sqft)",
       "remaining_residential_units_capacity = parcel.residential_units_capacity - parcel.aggregate(building.residential_units)",
       
       "households_per_parcel = parcel.number_of_agents(household)",
       "number_of_buildings = parcel.number_of_agents(building)",
       "built_area = parcel.aggregate(building.land_area, intermediates=[parcel])",
       "area_capacity = parcel.parcel_sqft - parcel.aggregate(building.land_area, intermediates=[parcel])",
           ]
