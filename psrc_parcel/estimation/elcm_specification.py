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
     ("bias_hb = urbansim_parcel.job_x_building.ln_sampling_probability_for_bias_correction_mnl_vacant_home_based_job_space", "bias", 1),
     ("bias_nhb = urbansim_parcel.job_x_building.ln_sampling_probability_for_bias_correction_mnl_vacant_non_home_based_job_space", "bias", 1),
    "distance_to_hwy = building.disaggregate(psrc.parcel.distance_to_highway_in_gridcell)",
    "is_near_highway = building.disaggregate(psrc.parcel.is_near_highway_in_gridcell)",    
    "distance_to_art = building.disaggregate(psrc.parcel.distance_to_arterial_in_gridcell)",
    "is_near_art = building.disaggregate(psrc.parcel.is_near_arterial_in_gridcell)",
    "ln_bldgage=ln(urbansim_parcel.building.age_masked)",
    "is_pre_1940 = building.year_built < 1940",    
    "lnsqft=ln(urbansim_parcel.building.building_sqft)",
    "lnsqftunit=ln(urbansim_parcel.building.building_sqft_per_unit)",
    "lnlotsqft=ln(urbansim_parcel.building.parcel_sqft)",
    "lnlotsqftunit=ln(urbansim_parcel.building.parcel_sqft_per_unit)",
    "ln_invfar=ln(urbansim_parcel.building.parcel_sqft/(urbansim_parcel.building.building_sqft).astype(float32))",
    "far=(urbansim_parcel.building.building_sqft/urbansim_parcel.building.parcel_sqft).astype(float32)",
    "unit_price = urbansim_parcel.building.unit_price",
    "ln_unit_price = ln(urbansim_parcel.building.unit_price)",
    "is_unit_price_le_0 = urbansim_parcel.building.unit_price <= 0",
    "ln_unit_price_trunc = ln(where(building.disaggregate(urbansim_parcel.parcel.unit_price<1500),where(building.disaggregate(urbansim_parcel.parcel.unit_price<1),1,building.disaggregate(urbansim_parcel.parcel.unit_price)),1500))",
    "avg_unit_price = building.disaggregate(zone.aggregate(urbansim_parcel.building.unit_price,function=mean,intermediates=[parcel]))",
    "lngcdacbd=ln(building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_seattle_cbd))",
    "lngcdacbdbell=ln(building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_bellevue_cbd))",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp20da=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp10da=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "lnemp20tw=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "hbwavgtmda = building.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",    
    "lnavginc=ln(building.disaggregate(urbansim_parcel.zone.average_income))",
    "lnempden=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_per_acre))",
    "lnpopden=ln(building.disaggregate(urbansim_parcel.zone.population_per_acre))",
    "inugb = building.disaggregate(parcel.is_inside_urban_growth_boundary)*1",
    "is_commercial_building = urbansim.building.is_commercial",
    "is_industrial_building = urbansim.building.is_industrial",
    "is_office_building = urbansim.building.is_office",
    "is_mixed_use_building = urbansim.building.is_mixed_use",
    "is_sfh_building = urbansim.building.is_single_family_residential",
    "is_mfh_building = urbansim.building.is_multi_family_residential",
    "ln_zone_empden_1=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_1)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_2=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_2)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_3=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_3)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_4=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_4)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_5=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_5)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_6=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_6)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_7=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_7)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_8=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_8)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_9=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_9)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_10=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_10)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_11=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_11)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_12=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_12)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_13=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_13)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_14=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_14)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_15=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_15)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_16=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_16)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_17=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_17)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_18=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_18)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_19=ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_of_sector_19)/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_service=ln(building.disaggregate(zone.aggregate(urbansim.job.is_in_employment_sector_group_service))/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_retail=ln(building.disaggregate(zone.aggregate(urbansim.job.is_in_employment_sector_group_retail))/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_zone_empden_basic=ln(building.disaggregate(zone.aggregate(urbansim.job.is_in_employment_sector_group_basic))/building.disaggregate(zone.aggregate(parcel.parcel_sqft)/43560.0))",
    "ln_job_sqft_x_bldg_sqft_per_job = ln(urbansim_parcel.job.sqft_imputed * urbansim_parcel.building.building_sqft_per_job)"
                 ]

specification = {}

specification["home_based"] = {
    "_definition_": all_variables,                               
    -2:   #Home-based
            [
     "bias_hb",
    "unit_price",      
#    "urbansim_parcel.building.age_masked",
    "lnsqftunit",
    "lnavginc",
    "lnpopden",
    "lnempden",
    "lngcdacbd",
    "lngcdacbdbell"
#    "urbansim_parcel.building.residential_units",
#    "households_in_zone = building.disaggregate(urbansim_parcel.zone.number_of_households, [parcel])",
#    "lot_area = building.disaggregate(parcel.parcel_sqft)",             
#    "average_income_in_zone = building.disaggregate(urbansim_parcel.zone.average_income, [parcel])",
#    "employment_of_sector_retailent_in_zone = building:opus_core.func.disaggregate(urbansim_parcel.zone.employment_of_sector_retailent,[parcel])",             
    ],                             
}

specification["non_home_based"] = {
    "_definition_": all_variables,                                   
        1:   # mining
            [
     "bias_nhb",
##    "ln_invfar",
     "far",
#    "ln_zone_empden_1",
    #"ln_unit_price_trunc",
    #"is_near_highway",    
    #"is_near_art",
    #"ln_bldgage",
    #"lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    #"lnavginc", #ln(zone.average_income),
    #"lnempden", #ln(zone.number_of_jobs_per_acre),
    #"lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    #"is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
    ],

        2: # construction
            [
     "bias_nhb",
##    "ln_invfar",
     "far",
#    "ln_zone_empden_2",
    "ln_unit_price_trunc",
    #"is_near_highway",    
#    "is_near_art",
    #"ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    #"lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",
    "is_commercial_building",
    "is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    "ln_zone_empden_service",
    "ln_zone_empden_basic",
    "lngcdacbdbell"
   ],
        3: # aerospace
            [
     "bias_nhb",
 ##   "ln_invfar",
     "far",
   "ln_zone_empden_3",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
    #"ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    #"lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    "is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        4: # other durable goods
            [
     "bias_nhb",
##    "ln_invfar",
     "far",
#    "ln_zone_empden_4",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
    "ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",
    "is_commercial_building",
    "is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        5: # non-durable goods
            [
     "bias_nhb",
##    "ln_invfar",
     "far",
#    "ln_zone_empden_5",
    #"avg_unit_price",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
    "ln_bldgage",
    "lnsqft",
   "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",
    "is_commercial_building",
    "is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        6: # whole sale trade
            [
     "bias_nhb",
#    "ln_invfar",
     "far",
#    "ln_zone_empden_6",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
    #"ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    "is_commercial_building",
    "is_industrial_building",
    #"is_office_building",
#    "is_mixed_use_building",
    "ln_zone_empden_service",
    #"ln_zone_empden_retail",
    "ln_zone_empden_basic",
    "ln_job_sqft_x_bldg_sqft_per_job",
        "lngcdacbdbell"
   ],
        7: # retail
            [
    # "bias_nhb",
    #"ln_invfar",
   # "far",
#    "ln_zone_empden_7",
    "ln_unit_price_trunc",
 #   "is_near_highway",    
 #   "is_near_art",
    #"ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    "inugb", #is_inside_urban_growth_boundary",
    "is_commercial_building",
    "is_industrial_building",
   # "is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        8: # transportation and warehousing
            [
     "bias_nhb",
#    "ln_invfar",
    # "far",
#    "ln_zone_empden_8",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
   # "ln_bldgage",
    "lnsqft",
    #"lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #inugb", #is_inside_urban_growth_boundary",
    "is_commercial_building",
    #"is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        9: # utilities
            [
     "bias_nhb",
#    "ln_invfar",
    # "far",
#    "ln_zone_empden_9",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
#    "ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
   # "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
   # "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    #"is_industrial_building",
    #"is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        10: # telecommunications
            [
     "bias_nhb",
#    "ln_invfar",
     "far",
#    "ln_zone_empden_10",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
#    "ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    #"is_industrial_building",
    #"is_office_building",
##    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        11: # other information
            [
     "bias_nhb",
#    "ln_invfar",
     "far",
#    "ln_zone_empden_11",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
#    "ln_bldgage",
    "lnsqft",
    #"lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    #"lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    #"is_industrial_building",
    #"is_office_building",
#    "is_mixed_use_building",
    "ln_zone_empden_service",
    "ln_zone_empden_retail",
    "ln_job_sqft_x_bldg_sqft_per_job",
        "lngcdacbdbell"
   ],
        12: # financial activities
            [
     "bias_nhb",
#    "ln_invfar",
     "far",
#    "ln_zone_empden_12",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
#    "ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    "is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        13: # professional and business
            [
     "bias_nhb",
#    "ln_invfar",
#    "ln_zone_empden_13",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
#    "ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    #"is_industrial_building",
    "is_office_building",
##    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        14: # food services and drinking places
            [
     "bias_nhb",
#    "ln_invfar",
     "far",
#    "ln_zone_empden_14",
    "ln_unit_price_trunc",
    "is_near_highway",    
    "is_near_art",
#    "ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    "is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    "lngcdacbdbell"
   ],
        15: # educational services
            [
     "bias_nhb",
     #"far",
    "ln_unit_price_trunc",
    "is_near_highway",    
    "is_near_art",
    "ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    "is_industrial_building",
    "is_office_building",
    #"is_mixed_use_building",
    "ln_zone_empden_service",
    #"ln_zone_empden_retail",
    "ln_job_sqft_x_bldg_sqft_per_job",
        "lngcdacbdbell"
   ],
           16: # health services
            [
     "bias_nhb",
     "far",
    "ln_unit_price_trunc",
    #"is_near_highway",    
    "is_near_art",
    "ln_bldgage",
    "lnsqft",
    "lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    #"lnemp10da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    "lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    "is_commercial_building",
    "is_industrial_building",
    "is_office_building",
    "is_mixed_use_building",
    "ln_zone_empden_service",
    "ln_zone_empden_retail",
    #"ln_job_sqft_x_bldg_sqft_per_job"
        "lngcdacbdbell"
   ],
        17: # other services
            [
     "bias_nhb",
#    "ln_invfar",
     "far",
#    "ln_zone_empden_17",
    "ln_unit_price_trunc",
#    "is_near_highway",    
#    "is_near_art",
#    "ln_bldgage",
    "lnsqft",
    #"lngcdacbd", #ln(generalized_cost_hbw_am_drive_alone_to_cbd),
    "lnemp30da", #ln(employment_within_30_minutes_travel_time_hbw_am_drive_alone),
    #"lnavginc", #ln(zone.average_income),
    "lnempden", #ln(zone.number_of_jobs_per_acre),
    "lnpopden", #ln(zone.population_per_acre),
    #"inugb", #is_inside_urban_growth_boundary",
    #"is_commercial_building",
    "is_industrial_building",
    "is_office_building",
#    "is_mixed_use_building",
    #"lngcdacbdbell"
   ],
}
