#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 


all_variables = [
    "distance_to_hwy = building.disaggregate(psrc.parcel.distance_to_highway_in_gridcell)",
    "is_near_highway = building.disaggregate(psrc.parcel.is_near_highway_in_gridcell)",    
    "distance_to_art = building.disaggregate(psrc.parcel.distance_to_arterial_in_gridcell)",
    "is_near_art = building.disaggregate(psrc.parcel.is_near_arterial_in_gridcell)",
    "ln_bldgage=ln(urbansim_parcel.building.age_masked)",
    "is_pre_1940 = building.year_built < 1940",    
    "lnsqft=ln(urbansim_parcel.building.building_sqft)",
    "lnsqftunit=ln(urbansim_parcel.building.building_sqft/building.residential_units)",
    "lnlotsqft=ln(building.disaggregate(parcel.parcel_sqft))",
    "lnlotsqftunit=ln(building.disaggregate(parcel.parcel_sqft)/building.residential_units)",
    "ln_invfar=ln(building.disaggregate(parcel.parcel_sqft)/urbansim_parcel.building.building_sqft)",
    "unit_price = building.disaggregate(urbansim_parcel.parcel.unit_price)",
    
    "lngcdacbd=ln(building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd, [parcel]))",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone, [parcel]))",
    "lnemp20da=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone, [parcel]))",
    "lnemp10da=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone, [parcel]))",
    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk, [parcel]))",
    "lnemp20tw=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk, [parcel]))",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk, [parcel]))",
    "hbwavgtmda = building.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone, [parcel])",

    "ln_residential_units_within_walking_distance = ln(building.disaggregate(psrc.parcel.residential_units_within_walking_distance))",         
    "lnretempwa=ln(building.disaggregate(psrc.parcel.retail_sector_employment_within_walking_distance))",
    "lnavginc=ln(building.disaggregate(urbansim.zone.average_income, [parcel]))",
    "lnempden=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_per_acre, [parcel]))",
    "lnpopden=ln(building.disaggregate(psrc.zone.population_per_acre, [parcel]))",
    "inugb = building.disaggregate(parcel.is_inside_urban_growth_boundary)*1",
     
    "is_commercial_building = building.disaggregate(generic_building_type.generic_building_type_name, [building_type]) == 'commercial'",
    "is_industrial_building = building.disaggregate(generic_building_type.generic_building_type_name, [building_type]) == 'industrial'",
    "is_office_building = building.disaggregate(generic_building_type.generic_building_type_name, [building_type]) == 'office'",
    "is_mixed_use_building = building.disaggregate(generic_building_type.generic_building_type_name, [building_type]) == 'mixed_use'",
    "is_sfh_building = building.disaggregate(generic_building_type.generic_building_type_name, [building_type]) == 'single_family_residential'",
    "is_mfh_building = building.disaggregate(generic_building_type.generic_building_type_name, [building_type]) == 'multi_family_residential'",
     
                 ]

specification = {}

specification["home_based"] = {
    "_definition_": all_variables,                               
    -2:   #RETAIL/ENT
            [
    "unit_price",      
#    "urbansim_parcel.building.age_masked",
    "lnsqftunit",
    "lnavginc",
    "lnpopden",
    "lnempden",
    "lngcdacbd",
    
#    "urbansim_parcel.building.residential_units",
#    "households_in_zone = building.disaggregate(urbansim_parcel.zone.number_of_households, [parcel])",
#    "lot_area = building.disaggregate(parcel.parcel_sqft)",             
#    "average_income_in_zone = building.disaggregate(urbansim_parcel.zone.average_income, [parcel])",
#    "employment_of_sector_retailent_in_zone = building:opus_core.func.disaggregate(urbansim_parcel.zone.employment_of_sector_retailent,[parcel])",             
    ],                             
}

specification["non_home_based"] = {
    "_definition_": all_variables,                                   
        1:   
            [

    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
#    "ln_invfar",
    
#    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    #"is_commercial_building",
    #"is_industrial_building",
    #"is_office_building",
    #"is_mixed_use_building",
    "is_sfh_building",
    #"is_mfh_building",
                        
    ],

        2:
            [
    "unit_price",
    #"distance_to_hwy",
#    "is_near_highway",    
    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",

    #"is_commercial_building",
    #"is_industrial_building",
    #"is_office_building",
    #"is_mixed_use_building",
    "is_sfh_building",
    #"is_mfh_building",
   ],
        3:
            [
    "unit_price",
    #"distance_to_hwy",
#    "is_near_highway",    
    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    #"lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    #"lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",

    "ln_s3_jobs_in_zone=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_3,[parcel]))",

    #"is_commercial_building",
    #"is_industrial_building",
    "is_office_building",
    #"is_mixed_use_building",
#    "is_sfh_building",
    #"is_mfh_building",
   ],
        4:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        5:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        6:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        7:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        8:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        9:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        10:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        11:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        12:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        13:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        14:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        15:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        16:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        17:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        18:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
        19:
            [
    "unit_price",
    "distance_to_hwy",
#    "is_near_highway",    
#    "distance_to_art",
#    "is_near_art",
    "ln_bldgage",
#    "is_pre_1940",    
    "lnsqft",
#    "lnsqftunit",
#    "lnlotsqft",
#    "lnlotsqftunit",
    "ln_invfar",
    
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
#    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp20da", #ln(employment_within_20_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp10da", #ln(employment_within_10_minutes_travel_time_hbw_am_drive_alone),
#    "lnemp30tw", #ln(employment_within_30_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp20tw", #ln(employment_within_20_minutes_travel_time_hbw_am_transit_walk),
#    "lnemp10wa", #ln(employment_within_10_minutes_travel_time_hbw_am_walk),
#    "hbwavgtmda", #trip_weighted_average_time_hbw_from_home_am_drive_alone,
    
#    "lnretempwa", #ln(retail_sector_employment_within_walking_distance),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",

    "is_commercial_building",
   ],
}
