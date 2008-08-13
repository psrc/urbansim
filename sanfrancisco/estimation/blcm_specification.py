#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

#number of observation with valid price
##7, 'CIE', 3141
##8, 'MIPS', 18090
##13, 'PDR', 7345
##14, 'RETAIL/ENT', 12281
##17, 'VISITOR', 416

specification ={}
specification = {  
        1:
            [
#    "building.year_built",
    "ln_sqft= ln(building.building_sqft)",
    "ln_unit_price = ln(building.unit_price)",
    "age = urbansim_parcel.building.age_masked",    
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_hholds_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
#    "ln_jobs_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.employment,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#    "lot_area=building.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "ln_emp_20_min_lrt=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_lrt_travel_time,intermediates=[parcel]))",          
#    "ln_emp_20_min_hwy=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel]))",          
#    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "lrt_weighted_access_to_population=building.disaggregate(sanfrancisco.zone.lrt_travel_time_weighted_access_by_population,intermediates=[parcel])", 
    "ln_sector_1_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_1_from_building,intermediates=[parcel]))",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_4_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_4_from_building,intermediates=[parcel])",
#    "sanfrancisco.building.is_building_use_cie",
#    "sanfrancisco.building.is_building_use_med",
#    "sanfrancisco.building.is_building_use_mips",
#    "sanfrancisco.building.is_building_use_retailent",
#    "sanfrancisco.building.is_building_use_mixed",
#    "sanfrancisco.building.is_building_use_pdr",    
#    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#    "building.stories",
#    "building.structure_value",    
    ],

        2:
            [
#    "building.year_built",
    "ln_sqft= ln(building.building_sqft)",
    "ln_unit_price = ln(building.unit_price)",
#    "age = urbansim_parcel.building.age_masked",    
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_hholds_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.employment,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#    "lot_area=building.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "ln_emp_20_min_bus=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel]))",          
    "lrt_weighted_access_to_population=building.disaggregate(sanfrancisco.zone.lrt_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "ln_emp_20_min_hwy=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel]))",          
#    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "ln_sector_2_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_2_from_building,intermediates=[parcel]))",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_4_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_4_from_building,intermediates=[parcel])",
##    "sanfrancisco.building.is_building_use_cie",
#    "sanfrancisco.building.is_building_use_med",
#    "sanfrancisco.building.is_building_use_mips",
##    "sanfrancisco.building.is_building_use_retailent",
#    "sanfrancisco.building.is_building_use_mixed",
##    "sanfrancisco.building.is_building_use_pdr",    
#    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#    "building.stories",
#    "building.structure_value",    
    ],

    3:
            [
#    "building.year_built",
    "ln_sqft= ln(building.building_sqft)",
    "ln_unit_price = ln(building.unit_price)",
    "age = urbansim_parcel.building.age_masked",    
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "ln_hholds_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.employment,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#    "lot_area=building.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "ln_emp_20_min_bus=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel]))",          
    "lrt_weighted_access_to_population=building.disaggregate(sanfrancisco.zone.lrt_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "ln_emp_20_min_hwy=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel]))",          
#    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "ln_sector_3_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel]))",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_4_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_4_from_building,intermediates=[parcel])",
##    "sanfrancisco.building.is_building_use_cie",
#    "sanfrancisco.building.is_building_use_med",
#    "sanfrancisco.building.is_building_use_mips",
##    "sanfrancisco.building.is_building_use_retailent",
#    "sanfrancisco.building.is_building_use_mixed",
##    "sanfrancisco.building.is_building_use_pdr",    
#    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#    "building.stories",
#    "building.structure_value",    
    ],

    4:
            [
#    "building.year_built",
    "ln_sqft= ln(building.building_sqft)",
    "ln_unit_price = ln(building.unit_price)",
#    "age = urbansim_parcel.building.age_masked",    
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_hholds_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.employment,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#    "lot_area=building.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "ln_emp_20_min_bus=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel]))",          
#    "ln_emp_20_min_hwy=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel]))",          
    "lrt_weighted_access_to_population=building.disaggregate(sanfrancisco.zone.lrt_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "ln_sector_4_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel]))",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_4_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_4_from_building,intermediates=[parcel])",
##    "sanfrancisco.building.is_building_use_cie",
#    "sanfrancisco.building.is_building_use_med",
#    "sanfrancisco.building.is_building_use_mips",
##    "sanfrancisco.building.is_building_use_retailent",
#    "sanfrancisco.building.is_building_use_mixed",
##    "sanfrancisco.building.is_building_use_pdr",    
#    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#    "building.stories",
#    "building.structure_value",    
    ],

    5:
            [
#    "building.year_built",
    "ln_sqft= ln(building.building_sqft)",
    "ln_unit_price = ln(building.unit_price)",
    "age = urbansim_parcel.building.age_masked",    
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_hholds_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.employment,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#    "lot_area=building.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "ln_emp_20_min_bus=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel]))",          
#    "ln_emp_20_min_hwy=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel]))",          
    "lrt_weighted_access_to_population=building.disaggregate(sanfrancisco.zone.lrt_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "ln_sector_5_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_5_from_building,intermediates=[parcel]))",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_4_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_4_from_building,intermediates=[parcel])",
##    "sanfrancisco.building.is_building_use_cie",
#    "sanfrancisco.building.is_building_use_med",
#    "sanfrancisco.building.is_building_use_mips",
##    "sanfrancisco.building.is_building_use_retailent",
#    "sanfrancisco.building.is_building_use_mixed",
##    "sanfrancisco.building.is_building_use_pdr",    
#    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#    "building.stories",
#    "building.structure_value",    
    ],

    6:
            [
#    "building.year_built",
    "ln_sqft= ln(building.building_sqft)",
    "ln_unit_price = ln(building.unit_price)",
#    "age = urbansim_parcel.building.age_masked",    
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_hholds_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(building.disaggregate(sanfrancisco.zone.employment,intermediates=[parcel])/(building.disaggregate(sanfrancisco.parcel.area)*0.0000229568411))", 
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#    "lot_area=building.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "ln_emp_20_min_bus=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel]))",          
#    "ln_emp_20_min_hwy=ln(building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel]))",          
    "lrt_weighted_access_to_population=building.disaggregate(sanfrancisco.zone.lrt_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "ln_sector_6_employment_in_zone=ln(building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_6_from_building,intermediates=[parcel]))",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_4_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_4_from_building,intermediates=[parcel])",
##    "sanfrancisco.building.is_building_use_cie",
#    "sanfrancisco.building.is_building_use_med",
#    "sanfrancisco.building.is_building_use_mips",
##    "sanfrancisco.building.is_building_use_retailent",
#    "sanfrancisco.building.is_building_use_mixed",
##    "sanfrancisco.building.is_building_use_pdr",    
#    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#    "building.stories",
#    "building.structure_value",    
    ],

}            
