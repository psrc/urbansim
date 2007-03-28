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
        8:   #MIPS
            [
#    "constant",
    "parcel.area",
    "parcel.land_value",    
#    
    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "employment_of_sector_mips_in_zone=parcel.disaggregate(sanfrancisco.zone.employment_of_sector_mips,intermediates=[parcel])",             
    "businesses_of_sector_mips_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_mips,intermediates=[parcel])",             
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    ],
    9:   #RETAIL/ENT
            [
#    "constant",
    "parcel.area",
    "parcel.land_value",    
#    
    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "employment_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.employment_of_sector_retailent,intermediates=[parcel])",             
#    "businesses_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_retailent,intermediates=[parcel])",             
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    ],
}            

specification['residential'] = {
    1:   #APT
            [
#    "constant",
#    "parcel.area",
#    "parcel.land_value",    
#    
#    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "hwy_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "hwy_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             

    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "employment_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.employment_of_sector_retailent,intermediates=[parcel])",             
#    "businesses_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_retailent,intermediates=[parcel])",             
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    ],

    2:   #CONDO
            [
#    "constant",
#    "parcel.area",
    "parcel.land_value",    
#    
    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
#    "hwy_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "hwy_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "employment_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.employment_of_sector_retailent,intermediates=[parcel])",             
#    "businesses_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_retailent,intermediates=[parcel])",             
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    ],

    3:   #FLATS
            [
#    "constant",
    "parcel.area",
#    "parcel.land_value",    
#    
    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_60_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_60_minutes_bus_travel_time,intermediates=[parcel])",             
##    "employment_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.employment_of_sector_retailent,intermediates=[parcel])",             
    "businesses_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_retailent,intermediates=[parcel])",             
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    ],
    5:   #SINGLE
            [
#    "constant",
#    "parcel.area",
#    "parcel.land_value",    
#    
    "households_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
#    "lot_area=parcel.disaggregate(parcel.area)",             
#    "bus_travel_time_weighted_access_by_population=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
#    "bus_travel_time_weighted_access_to_employment=parcel.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_bus_travel_time=parcel.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,intermediates=[parcel])",             
#    "employment_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.employment_of_sector_retailent,intermediates=[parcel])",             
#    "businesses_of_sector_retailent_in_zone=parcel.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_retailent,intermediates=[parcel])",             
    
    "average_income_in_zone=parcel.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    ],

}
