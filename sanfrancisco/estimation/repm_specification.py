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

#number of observation with valid price
##+-----------------+--------------+----------+
##| building_use_id | building_use | count(*) |
##+-----------------+--------------+----------+
##|               1 | APTS         |     2544 |
##|               2 | CONDO        |     3103 |
##|               3 | FLATS        |     1982 |
##|               4 | LIVEWORK     |      242 |
##|               5 | SINGLE       |    12819 |
##|               6 | SRO          |       47 |
##|               7 | CIE          |       31 |
##|               8 | MIPS         |      469 |
##|               9 | MIXED        |      563 |
##|              10 | MIXRES       |     2011 |
##|              11 | OPENSPACE    |        3 |
##|              13 | PDR          |      211 |
##|              14 | RETAILENT   |      279 |
##|              16 | VACANT       |       20 |
##|              17 | VISITOR      |       12 |
##+-----------------+--------------+----------+

specification ={}
specification = {  
        1:   #APT
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
        
#    "building.building_sqft",
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
    "ln_sqft_unit = ln(building.building_sqft/building.residential_units)",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area_unit= ln(building.disaggregate(parcel.area)/building.residential_units)", 
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])", 
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
#    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
#    "sector_3_employment_in_zone=building.disaggregate(zone.aggregate(sanfrancisco.building.employment_of_sector_3,intermediates=[parcel]), intermediates=[parcel])",    
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",        
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#    

#    "building.stories",
#    "building.structure_value",    
    ],
    2:   #CONDO
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
#    "building.building_sqft",
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
    "ln_sqft_unit = ln(building.building_sqft/building.residential_units)",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area_unit= ln(building.disaggregate(parcel.area)/building.residential_units)", 
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])", 
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
#    "sector_3_employment_in_zone=building.disaggregate(zone.aggregate(sanfrancisco.building.employment_of_sector_3,intermediates=[parcel]), intermediates=[parcel])",    
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",        
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
#    

#    "building.stories",
#    "building.structure_value",    

    ],
    3:   #FLATS
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
#    "building.building_sqft",
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
    "ln_sqft_unit = ln(building.building_sqft/building.residential_units)",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area_unit= ln(building.disaggregate(parcel.area)/building.residential_units)", 
#    "hwy_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])", 
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
#    "sector_3_employment_in_zone=building.disaggregate(zone.aggregate(sanfrancisco.building.employment_of_sector_3,intermediates=[parcel]), intermediates=[parcel])",    
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",        
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    ],
    5:   #SINGLE
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
#    "building.building_sqft",
#    "far = building.building_sqft/building.disaggregate(parcel.area)",        
    "ln_sqft_unit = ln(building.building_sqft/building.residential_units)",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area_unit= ln(building.disaggregate(parcel.area)/building.residential_units)", 
#    "hwy_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])", 
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
#    "sector_3_employment_in_zone=building.disaggregate(zone.aggregate(sanfrancisco.building.employment_of_sector_3,intermediates=[parcel]), intermediates=[parcel])",    
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",        
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    ],

    7: # CIE
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
    "ln_sqft = ln(building.building_sqft)",
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area=ln(building.disaggregate(parcel.area))",
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
#    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#
##    "building.stories",
##    "building.structure_value",    
    ],

    8: #MIPS
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
    "ln_sqft = ln(building.building_sqft)",
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area=ln(building.disaggregate(parcel.area))",
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#
##    "building.stories",
##    "building.structure_value",    
    ],

    9:   #mixed 
            [
    "constant",
    "building.year_built",
#    
    "building.bedrooms",
#        
    "building.building_sqft",
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "lot_area=building.disaggregate(parcel.area)",
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",
    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",
#    "employment_within_20_minutes_bus_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#
##    "building.stories",
##    "building.structure_value",    
    ],    
    
    10:   #mixed residential
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
#    "building.building_sqft",
    "ln_sqft_unit = ln(building.building_sqft/building.residential_units)",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area_unit= ln(building.disaggregate(parcel.area)/building.residential_units)", 
#    "hwy_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])", 
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])", 
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
#    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
#    "sector_3_employment_in_zone=building.disaggregate(zone.aggregate(sanfrancisco.building.employment_of_sector_3,intermediates=[parcel]), intermediates=[parcel])",    
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",        
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",

    ],

    13:   #PDR
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
    "ln_sqft = ln(building.building_sqft)",
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area=ln(building.disaggregate(parcel.area))",
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#
##    "building.stories",
##    "building.structure_value",    
    ],

    14:   #RETAILENT
            [
    "constant",
#    "building.year_built",
    "age = psrc_parcel.building.age_masked",    
#    "building.bedrooms",
    "far = building.building_sqft/building.disaggregate(parcel.area)",        
    "ln_sqft = ln(building.building_sqft)",
#    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "ln_lot_area=ln(building.disaggregate(parcel.area))",
#    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",
#    "bus_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",
    "emp_20_min_bus=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",          
    "emp_20_min_hwy=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",          
    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#
##    "building.stories",
##    "building.structure_value",    
    ],        

}            
