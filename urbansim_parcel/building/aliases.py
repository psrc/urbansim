# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
#   "generic_unit_name = building.disaggregate(generic_building_type.unit_name, intermediates=[building_type])",
   "unit_name = building.disaggregate(building_type.unit_name)",
   "generic_building_type_id = building.disaggregate(building_type.generic_building_type_id)",
   "parcel_sqft = building.disaggregate(parcel.parcel_sqft)",
   "employment = building.number_of_agents(job)",
   "number_of_jobs = building.number_of_agents(job)",
   "number_of_households = building.number_of_agents(household)",
   "population = building.aggregate(household.persons)",
   "occupied_building_sqft_by_non_home_based_jobs = building.aggregate(urbansim_parcel.job.sqft_imputed * urbansim.job.is_building_type_non_home_based)",
   "building_type_name = building.disaggregate(building_type.building_type_name)",
   "is_residential = building.disaggregate(building_type.is_residential)",
   "are_units_building_sqft = building.non_residential_sqft > 0",
   "parcel_sqft_per_unit=safe_array_divide(building.disaggregate(parcel.parcel_sqft),building.residential_units)",
   "building_sqft_per_unit=safe_array_divide(urbansim_parcel.building.building_sqft,building.residential_units)",
   "unit_price = building.disaggregate(urbansim_parcel.parcel.unit_price)",
   "grid_id = building.disaggregate(parcel.grid_id)",
   "zone_id = building.disaggregate(parcel.zone_id)",
   "faz_id = building.disaggregate(zone.faz_id)",
   "large_area_id = building.disaggregate(faz.large_area_id, intermediates=[zone, parcel])",   
   "zip_id = building.disaggregate(parcel.zip_id)",
   "has_vacant_residential_units = urbansim_parcel.building.vacant_residential_units > 0",
   "is_governmental = building.disaggregate(building_type.generic_building_type_description == 'government')",
    ]

for group in ['retail', 'manu', 'wtcu', 'fires', 'gov', 'edu']:
    aliases.append("number_of_jobs_of_sector_group_%s = building.aggregate(urbansim.job.is_in_employment_sector_group_%s)" % (group, group))
    