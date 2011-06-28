# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

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
   "occupied_building_sqft_by_non_home_based_jobs = building.aggregate(urbansim_parcel.job.sqft_imputed * urbansim_parcel.job.is_non_home_based)",
   "building_type_name = building.disaggregate(building_type.building_type_name)",
   "is_residential = (building.disaggregate(building_type.is_residential)).astype('bool')",
   "is_non_residential = building.disaggregate(building_type.is_residential==0)",
   "are_units_building_sqft = building.non_residential_sqft > 0",
   "parcel_sqft_per_unit=safe_array_divide(building.disaggregate(parcel.parcel_sqft),building.residential_units)",
   "building_sqft_per_unit=safe_array_divide(urbansim_parcel.building.building_sqft,building.residential_units)",
   "unit_price = building.disaggregate(urbansim_parcel.parcel.unit_price)",
   "price_per_unit = building.disaggregate(urbansim_parcel.parcel.unit_price) * urbansim_parcel.building.building_sqft_per_unit",
    #"avg_price_per_unit_in_zone = building.disaggregate(zone.aggregate(urbansim_parcel.building.price_per_unit * urbansim_parcel.building.is_residential) / zone.aggregate(urbansim_parcel.building.is_residential),intermediates=[parcel] )",
   #"avg_price_per_unit_in_zone = building.disaggregate(zone.aggregate(urbansim_parcel.building.price_per_unit, function=mean, intermediates=[parcel]) )",
   "avg_price_per_unit_in_zone = building.disaggregate(zone.aggregate(urbansim_parcel.building.price_per_unit, function=sum, intermediates=[parcel])/zone.aggregate(parcel.number_of_agents(building)))",
   "avg_price_per_sqft_in_zone = building.disaggregate(zone.aggregate(urbansim_parcel.building.unit_price, function=mean, intermediates=[parcel]) )",
   "avg_price_per_sqft_in_faz  = building.disaggregate( faz.aggregate(urbansim_parcel.building.unit_price, function=mean, intermediates=[parcel, zone]) )",
   "grid_id = building.disaggregate(parcel.grid_id)",
   "zone_id = building.disaggregate(parcel.zone_id)",
   "faz_id = building.disaggregate(zone.faz_id)",
   "large_area_id = building.disaggregate(faz.large_area_id, intermediates=[zone, parcel])",
   "zip_id = building.disaggregate(parcel.zip_id)",
   "has_vacant_residential_units = urbansim_parcel.building.vacant_residential_units > 0",
   "is_governmental = building.disaggregate(building_type.generic_building_type_description == 'government')",
   "occupied_building_sqft = numpy.minimum(urbansim_parcel.building.occupied_building_sqft_by_non_home_based_jobs, building.building_sqft)",
   "occupied_residential_units = numpy.minimum(building.number_of_agents(household), building.residential_units)",
    ]

for group in ['retail', 'manu', 'wtcu', 'fires', 'gov', 'edu']:
    aliases.append("number_of_jobs_of_sector_group_%s = building.aggregate(urbansim.job.is_in_employment_sector_group_%s)" % (group, group))

