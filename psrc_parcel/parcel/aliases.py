# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
       "is_redevelopable=(parcel.number_of_agents(building)>0)*(urbansim_parcel.parcel.improvement_value / ( urbansim_parcel.parcel.unit_price * urbansim_parcel.parcel.existing_units ) < 0.1)*(parcel.aggregate(urbansim_parcel.building.age_masked, function=mean)>30)",       
       "total_price=parcel.land_value+parcel.aggregate(building.improvement_value)",
       "yard_sqft_per_unit = safe_array_divide( parcel.parcel_sqft-parcel.aggregate(building.land_area), (urbansim_parcel.parcel.residential_units).astype(float32) )",
       "yard_per_sqft = safe_array_divide( parcel.parcel_sqft-parcel.aggregate(building.land_area), parcel.parcel_sqft)",
       "residential_units = parcel.aggregate(building.residential_units)",
       "number_of_private_schools = parcel.aggregate(school.public==0)",
       "number_of_public_schools = parcel.aggregate(school.public)",
       "number_of_schools = parcel.number_of_agents(school)",
       "number_of_good_public_schools = parcel.aggregate(school.public * (school.total_score >= 8))",
       "population = urbansim_parcel.parcel.population",
       "acres_wwd = psrc_parcel.parcel.psrc_parcel_package_parcel_sqft_wwd / 43560.0",
       "employment_density_within_walking_distance = psrc_parcel.parcel.urbansim_parcel_package_number_of_jobs_wwd/psrc_parcel.parcel.acres_wwd",
       "population_density_within_walking_distance = psrc_parcel.parcel.urbansim_parcel_package_population_wwd/psrc_parcel.parcel.acres_wwd",
       "retail_density_within_walking_distance = psrc_parcel.parcel.urbansim_parcel_package_employment_retail_wwd/psrc_parcel.parcel.acres_wwd",
       "is_park = numpy.logical_or(parcel.land_use_type_id == 19, parcel.land_use_type_id == 21)",
       "park_area = parcel.parcel_sqft * psrc_parcel.parcel.is_park",
       "number_of_poor_households = parcel.aggregate(psrc_parcel.household.is_poor, intermediates=[building])",
       "number_of_wealthy_households = parcel.aggregate(psrc_parcel.household.is_wealthy, intermediates=[building])",
       "percent_poverty_wwd = safe_array_divide(psrc_parcel.parcel.psrc_parcel_package_number_of_poor_households_wwd, psrc_parcel.parcel.urbansim_parcel_package_number_of_households_wwd)",
       "percent_wealth_wwd = safe_array_divide(psrc_parcel.parcel.psrc_parcel_package_number_of_wealthy_households_wwd, psrc_parcel.parcel.urbansim_parcel_package_number_of_households_wwd)",
       "developable_capacity = clip_to_zero(psrc_parcel.parcel.max_developable_capacity-urbansim_parcel.parcel.building_sqft)",
       "building_density_wwd = psrc_parcel.parcel.urbansim_parcel_package_building_sqft_wwd / psrc_parcel.parcel.psrc_parcel_package_parcel_sqft_wwd",
       "avg_zonal_parcel_sqft = parcel.disaggregate(zone.aggregate(parcel.parcel_sqft)/zone.number_of_agents(parcel))",
       "is_lut_19_25_26 = (parcel.land_use_type_id == 19) + (parcel.land_use_type_id == 25) + (parcel.land_use_type_id == 26)",
       "existing_units = (urbansim_parcel.parcel.building_sqft > 0)*urbansim_parcel.parcel.building_sqft + (urbansim_parcel.parcel.building_sqft <= 0)*parcel.parcel_sqft"
           ]


