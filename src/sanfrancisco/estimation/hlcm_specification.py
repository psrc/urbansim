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
 
specification ={} 
specification = {   
 
1:   #submodel 
          [         
#            "is_pre_1940 = building.year_built < 1940",
#             "far = building.building_sqft/building.disaggregate(parcel.area)",        
             "ln_residential_units=ln(building.residential_units)",
#             "cost_income = household.income * building.unit_price / 1000000",
#             "ln_price = ln(building.unit_price)",
              "ln_inc_minus_cost = ln_bounded((household.income*1000) - (building.unit_price/10))",
#             "condo = (building.building_use_id == 2)",
#             "apartment = (building.building_use_id == 1)",  
#             "inc_condo = household.income * (building.building_use_id == 1)",
#             "inc_apt = household.income * (building.building_use_id == 2)",
#             "building.year_built", 
#             "building.bedrooms", 
#             "sanfrancisco.building.building_sqft",        
#             "ln_avg_building_sf_per_unit = ln(sanfrancisco.building.building_sqft/building.residential_units)",
             "ln_inc_building_sf_per_unit = ln(household.income * sanfrancisco.building.building_sqft/building.residential_units)",
#             "building_sqft_per_unit=sanfrancisco.building.building_sqft / sanfrancisco.building.residential_units", 
             "ln_households_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel]))", 
#             "lot_area=building.disaggregate(parcel.area)", 
             "ln_emp_30_bus = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_bus_travel_time,intermediates=[parcel]))", 
#             "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])", 
#             "ln_sector_3_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
             "ln_inc_sector_3_employment_in_zone=ln(household.income * building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
#             "employment_of_building_use_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_building_use_cie,intermediates=[parcel])",              
#             "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#             "income_ratio = household.income / building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#             "avg_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
             "ln_inc_avg_inc = ln(household.income * building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
            ], 
2:   #submodel 
          [         
#            "is_pre_1940 = building.year_built < 1940",
#             "far = building.building_sqft/building.disaggregate(parcel.area)",        
             "ln_residential_units=ln(building.residential_units)",
#             "cost_income = household.income * building.unit_price / 1000000",
#             "ln_price = ln(building.unit_price)",
              "ln_inc_minus_cost = ln_bounded((household.income*1000) - (building.unit_price/10))",
#             "condo = (building.building_use_id == 2)",
#             "apartment = (building.building_use_id == 1)",  
#             "inc_condo = household.income * (building.building_use_id == 1)",
#             "inc_apt = household.income * (building.building_use_id == 2)",
#             "building.year_built", 
#             "building.bedrooms", 
#             "sanfrancisco.building.building_sqft",        
#             "ln_avg_building_sf_per_unit = ln(sanfrancisco.building.building_sqft/building.residential_units)",
             "ln_inc_building_sf_per_unit = ln(household.income * sanfrancisco.building.building_sqft/building.residential_units)",
#             "building_sqft_per_unit=sanfrancisco.building.building_sqft / sanfrancisco.building.residential_units", 
             "ln_households_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel]))", 
#             "lot_area=building.disaggregate(parcel.area)", 
             "ln_emp_30_bus = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_bus_travel_time,intermediates=[parcel]))", 
#             "ln_emp_30_hwy = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_hwy_travel_time,intermediates=[parcel]))", 
#             "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])", 
#             "ln_sector_3_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
             "ln_inc_sector_3_employment_in_zone=ln(household.income * building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
#             "employment_of_building_use_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_building_use_cie,intermediates=[parcel])",              
#             "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#             "income_ratio = household.income / building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#             "avg_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
             "ln_inc_avg_inc = ln(household.income * building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
            ], 
3:   #submodel 
          [         
#            "is_pre_1940 = building.year_built < 1940",
#             "far = building.building_sqft/building.disaggregate(parcel.area)",        
             "ln_residential_units=ln(building.residential_units)",
#             "cost_income = household.income * building.unit_price / 1000000",
#             "ln_price = ln(building.unit_price)",
              "ln_inc_minus_cost = ln_bounded((household.income*1000) - (building.unit_price/10))",
#             "condo = (building.building_use_id == 2)",
#             "apartment = (building.building_use_id == 1)",  
#             "inc_condo = household.income * (building.building_use_id == 1)",
#             "inc_apt = household.income * (building.building_use_id == 2)",
#             "building.year_built", 
#             "building.bedrooms", 
#             "sanfrancisco.building.building_sqft",        
#             "ln_avg_building_sf_per_unit = ln(sanfrancisco.building.building_sqft/building.residential_units)",
             "ln_inc_building_sf_per_unit = ln(household.income * sanfrancisco.building.building_sqft/building.residential_units)",
#             "building_sqft_per_unit=sanfrancisco.building.building_sqft / sanfrancisco.building.residential_units", 
             "ln_households_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel]))", 
#             "lot_area=building.disaggregate(parcel.area)", 
#             "ln_emp_30_bus = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_bus_travel_time,intermediates=[parcel]))", 
             "ln_emp_30_hwy = ln(building.disaggregate(sanfrancisco.zone.employment_within_30_minutes_hwy_travel_time,intermediates=[parcel]))", 
#             "ln_sector_3_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
             "ln_inc_sector_3_employment_in_zone=ln(household.income * building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
#             "employment_of_building_use_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_building_use_cie,intermediates=[parcel])",              
#             "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#             "income_ratio = household.income / building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#             "avg_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
             "ln_inc_avg_inc = ln(household.income * building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
            ], 
 
}             
