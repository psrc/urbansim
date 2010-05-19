# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
       "number_of_businesses = parcel.aggregate(sanfrancisco.building.number_of_businesses)",
       "employment = parcel.aggregate(sanfrancisco.building.employment)",
       "number_of_households = parcel.aggregate(sanfrancisco.building.number_of_households)",
       "population = parcel.aggregate(sanfrancisco.building.population)", 
       "building_sqft_per_unit = safe_array_divide(parcel.building_sqft, parcel.residential_units)",
       "building_sqft = parcel.aggregate(building.building_sqft)",
       "housing_value = safe_array_divide((parcel.land_val + parcel.struc_val), sanfrancisco.parcel.residential_units)",
       "lot_sqft_per_unit = safe_array_divide(parcel.lot_sf, parcel.residential_units)",
       "residential_units = parcel.aggregate(building.residential_units)",
           ]