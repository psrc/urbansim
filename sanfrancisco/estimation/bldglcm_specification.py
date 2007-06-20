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
##7, 'CIE', 3141
##8, 'MIPS', 18090
##13, 'PDR', 7345
##14, 'RETAIL/ENT', 12281
##17, 'VISITOR', 416

specification ={}
specification['nonresidential'] = {  
        7:   #CIE
            [
    "ln_land_area = ln(parcel.area)",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
#    "parcel.land_value",    
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#     "ln_sqft = ln(parcel.aggregate(building.building_sqft, function=sum))",

#    "ln_price = ln(sanfrancisco.building.unit_price)",
#    "sanfrancisco.building.unit_price",
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households)",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "sector_3_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building)",    
#    "sector_4_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
    "ln_avg_income_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.average_income))",
    
#    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    #"sanfrancisco.building.building_sqft_capacity",
    #"building.residential_units_capacity",
    ],

        8:   #MIPS
            [
    "ln_land_area = ln(parcel.area)",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
#    "parcel.land_value",    
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#     "ln_sqft = ln(parcel.aggregate(building.building_sqft, function=sum))",
    "ln_avg_income_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.average_income))",

#    "ln_price = ln(sanfrancisco.building.unit_price)",
#    "sanfrancisco.building.unit_price",
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households)",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "sector_3_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building)",    
#    "sector_4_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    
#    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    #"sanfrancisco.building.building_sqft_capacity",
    #"building.residential_units_capacity",
    ],
    9:   #MIXED
            [
    "ln_land_area = ln(parcel.area)",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
#    "parcel.land_value",    
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#     "ln_sqft = ln(parcel.aggregate(building.building_sqft, function=sum))",
    "ln_avg_income_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.average_income))",

#    "ln_price = ln(sanfrancisco.building.unit_price)",
#    "sanfrancisco.building.unit_price",
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households)",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "sector_3_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building)",    
#    "sector_4_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    
#    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    #"sanfrancisco.building.building_sqft_capacity",
    #"building.residential_units_capacity",
    ],
        13:   #PDR
            [
    "ln_land_area = ln(parcel.area)",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
#    "parcel.land_value",    
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#     "ln_sqft = ln(parcel.aggregate(building.building_sqft, function=sum))",
    "ln_avg_income_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.average_income))",

#    "ln_price = ln(sanfrancisco.building.unit_price)",
#    "sanfrancisco.building.unit_price",
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households)",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "sector_3_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building)",    
#    "sector_4_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    
#    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    #"sanfrancisco.building.building_sqft_capacity",
    #"building.residential_units_capacity",
    ],

        14:   #'RETAIL/ENT'
            [
    "ln_land_area = ln(parcel.area)",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
#    "parcel.land_value",    
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#     "ln_sqft = ln(parcel.aggregate(building.building_sqft, function=sum))",
    "ln_avg_income_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.average_income))",

#    "ln_price = ln(sanfrancisco.building.unit_price)",
#    "sanfrancisco.building.unit_price",
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households)",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "sector_3_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building)",    
#    "sector_4_employment_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=parcel.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    
#    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    #"sanfrancisco.building.building_sqft_capacity",
    #"building.residential_units_capacity",
    ],
    
}            

specification['residential'] = {
    1:   #APT
            [
#    "ln_land_area_unit = ln(parcel.area/parcel.aggregate(sanfrancisco.building.residential_units))",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
    "ln_land_area = ln(parcel.area)",
#    "parcel.land_value",    
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income)",
    "ln_avg_income_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.average_income))",
    ],

    2:   #CONDO
            [
#    "ln_land_area_unit = ln(parcel.area/parcel.aggregate(sanfrancisco.building.residential_units))",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
#    "parcel.land_value",    
    "ln_land_area = ln(parcel.area)",
#     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#    "ln_price = ln(sanfrancisco.building.unit_price)",
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income)",
    ],

    3:   #FLATS
            [
#    "ln_land_area_unit = ln(parcel.area/parcel.aggregate(sanfrancisco.building.residential_units))",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
#    "parcel.land_value",  
#    "ln_land_area = ln(parcel.area)",
#     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#    "ln_price = ln(sanfrancisco.building.unit_price)",
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income)",
    ],
    5:   #SINGLE
            [
#    "ln_land_area_unit = ln(parcel.area/parcel.aggregate(sanfrancisco.building.residential_units))",
    "ln_hholds_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.number_of_households)/(parcel.area*0.0000229568411))", 
    "ln_jobs_per_acre_in_zone=ln(parcel.disaggregate(sanfrancisco.zone.employment)/(parcel.area*0.0000229568411))", 
#    "parcel.land_value",
    "ln_land_area = ln(parcel.area)",
#     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#    "ln_price = ln(sanfrancisco.building.unit_price)",
     "ln_price = ln(parcel.aggregate(building.unit_price, function=mean))",
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "sector_3_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_3_from_building,intermediates=[parcel])",    
#    "sector_4_employment_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_employment_of_sector_4_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "sector_3_businesses_in_zone=building.disaggregate(sanfrancisco.zone.aggregate_number_of_businesses_of_sector_3_from_building,intermediates=[parcel])",
#    "ln_avg_income_in_zone=ln(building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel]))",
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income)",
    ],

}
