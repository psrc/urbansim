# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
 
variable_aliases = [
             "bias_correction = urbansim_parcel.household_x_building.ln_sampling_probability_for_bias_correction_mnl_vacant_residential_units",
#            "is_pre_1940 = building.year_built < 1940",
#             "far = building.building_sqft/building.disaggregate(parcel.area)",        
             "ln_residential_units=ln(building.residential_units)",
#             "cost_income = household.income * building.unit_price / 1000000",
#             "ln_price = ln(building.unit_price)",
              "ln_inc_minus_cost = ln_bounded((household.income*1000) - (building.unit_price/10))",
             "condo = (building.building_use_id == 2)",
             "apartment = (building.building_use_id == 1)",  
             "single_family = (building.building_use_id == 5)",  
             "inc_condo = household.income * (building.building_use_id == 1)",
             "inc_apt = household.income * (building.building_use_id == 2)",
             "inc_single_family = household.income * (building.building_use_id == 5)",
             "building.year_built", 
#             "building.bedrooms", 
#             "sanfrancisco.building.building_sqft",        
             "ln_avg_building_sf_per_unit = ln(sanfrancisco.building.building_sqft/building.residential_units)",
             "ln_inc_building_sf_per_unit = ln(household.income * sanfrancisco.building.building_sqft/building.residential_units)",
#             "building_sqft_per_unit=sanfrancisco.building.building_sqft / sanfrancisco.building.residential_units", 
             "ln_households_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel]))", 
#             "lot_area=building.disaggregate(parcel.area)", 
             "ln_lot_sf_per_unit = ln(building.disaggregate(parcel.area)/building.residential_units)",
             "ln_emp_30_bus = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_bus_travel_time,intermediates=[parcel]))", 
             "ln_emp_30_hwy = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_hwy_travel_time,intermediates=[parcel]))",
             "ln_emp_30_bart = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_bart_travel_time,intermediates=[parcel]))",
             "ln_emp_30_lrt = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_lrt_travel_time,intermediates=[parcel]))",
             "ln_emp_45_lrt = ln(building.disaggregate(sanfrancisco.zone.employment_within_45_minutes_lrt_travel_time,intermediates=[parcel]))",  
             "bus_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])", 
             "hwy_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])", 
#             "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])", 
#             "ln_sector_3_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
             "ln_inc_sector_3_employment_in_zone=ln(household.income * building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
#             "employment_of_building_use_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_building_use_cie,intermediates=[parcel])",              
             "ln_avg_income =ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
             "income_ratio = household.income / building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
             "avg_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
             "ln_inc_avg_inc = ln(household.income * building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
             "lnempden=(ln(building.disaggregate(sanfrancisco.zone.employment)/building.disaggregate(zone.aggregate(parcel.area)/43560.0)))",
             "lnpopden=(ln(building.disaggregate(sanfrancisco.zone.population)/building.disaggregate(zone.aggregate(parcel.area)/43560.0)))",
]

specification = {}

specification = {
"_definition_": variable_aliases,

1:   #submodel 
          [         
             "bias_correction",
#             "condo",
#             "apartment",
             "single_family",
#             "ln_residential_units",
             "lnempden",
             "lnpopden",
#             "far",
             "ln_inc_minus_cost",
             "ln_avg_building_sf_per_unit",
#             "ln_lot_sf_per_unit",
#             "ln_inc_building_sf_per_unit",
#             "ln_households_in_zone", 
             "ln_emp_30_lrt", 
#             "ln_emp_30_hwy",
#             "ln_inc_sector_3_employment_in_zone",    
             "ln_inc_avg_inc",
              "ln_avg_income",
            ], 
2:   #submodel 
          [         
             "bias_correction",
#             "condo",
#             "apartment",
             "single_family",
#             "ln_residential_units",
             "lnempden",
             "lnpopden",
             "ln_inc_minus_cost",
             "ln_avg_building_sf_per_unit",
#             "ln_lot_sf_per_unit",
#             "ln_inc_building_sf_per_unit",
#             "ln_households_in_zone", 
#             "ln_emp_30_hwy",
             "ln_emp_30_lrt",
#             "ln_inc_sector_3_employment_in_zone",    
             "ln_inc_avg_inc",
              "ln_avg_income",
            ], 
3:   #submodel 
          [         
             "bias_correction",
#             "condo",
#             "apartment",
             "single_family",
#             "ln_residential_units",
             "lnempden",
             "lnpopden",
             "ln_inc_minus_cost",
             "ln_avg_building_sf_per_unit",
#             "ln_lot_sf_per_unit",
#             "ln_emp_30_bus",
#             "ln_emp_45_lrt",
#              "hwy_weighted_access_to_employment",
#             "ln_inc_sector_3_employment_in_zone",    
             "ln_inc_avg_inc",
              "ln_avg_income",
            ], 
 
}             
