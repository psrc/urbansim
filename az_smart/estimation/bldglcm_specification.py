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
    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_households,[parcel]) as households_in_zone",
#    "parcel:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_of_sector_mips,[parcel]) as employment_of_sector_mips_in_zone",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_businesses_of_sector_mips,[parcel]) as businesses_of_sector_mips_in_zone",             
    
    "parcel:opus_core.func.disaggregate(az_smart.zone.average_income, [parcel]) as average_income_in_zone",
    ],
    9:   #RETAIL/ENT
            [
#    "constant",
    "parcel.area",
    "parcel.land_value",    
#    
    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_households,[parcel]) as households_in_zone",
#    "parcel:opus_core.func.disaggregate(parcel.area) as lot_area",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_of_sector_retailent,[parcel]) as employment_of_sector_retailent_in_zone",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_businesses_of_sector_retailent,[parcel]) as businesses_of_sector_retailent_in_zone",             
    
    "parcel:opus_core.func.disaggregate(az_smart.zone.average_income, [parcel]) as average_income_in_zone",
    ],
}            

specification['residential'] = {
    1:   #APT
            [
#    "constant",
#    "parcel.area",
#    "parcel.land_value",    
#    
#    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_households,[parcel]) as households_in_zone",
#    "parcel:opus_core.func.disaggregate(parcel.area) as lot_area",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.hwy_travel_time_weighted_access_by_population,[parcel]) as hwy_travel_time_weighted_access_by_population",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.hwy_travel_time_weighted_access_to_employment,[parcel]) as hwy_travel_time_weighted_access_to_employment",             

    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_of_sector_retailent,[parcel]) as employment_of_sector_retailent_in_zone",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_businesses_of_sector_retailent,[parcel]) as businesses_of_sector_retailent_in_zone",             
    
    "parcel:opus_core.func.disaggregate(az_smart.zone.average_income, [parcel]) as average_income_in_zone",
    ],

    2:   #CONDO
            [
#    "constant",
#    "parcel.area",
    "parcel.land_value",    
#    
    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_households,[parcel]) as households_in_zone",
#    "parcel:opus_core.func.disaggregate(parcel.area) as lot_area",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.hwy_travel_time_weighted_access_by_population,[parcel]) as hwy_travel_time_weighted_access_by_population",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.hwy_travel_time_weighted_access_to_employment,[parcel]) as hwy_travel_time_weighted_access_to_employment",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_of_sector_retailent,[parcel]) as employment_of_sector_retailent_in_zone",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_businesses_of_sector_retailent,[parcel]) as businesses_of_sector_retailent_in_zone",             
    
    "parcel:opus_core.func.disaggregate(az_smart.zone.average_income, [parcel]) as average_income_in_zone",
    ],

    3:   #FLATS
            [
#    "constant",
    "parcel.area",
#    "parcel.land_value",    
#    
    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_households,[parcel]) as households_in_zone",
#    "parcel:opus_core.func.disaggregate(parcel.area) as lot_area",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_within_60_minutes_bus_travel_time,[parcel]) as employment_within_60_minutes_bus_travel_time",             
##    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_of_sector_retailent,[parcel]) as employment_of_sector_retailent_in_zone",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_businesses_of_sector_retailent,[parcel]) as businesses_of_sector_retailent_in_zone",             
    
    "parcel:opus_core.func.disaggregate(az_smart.zone.average_income, [parcel]) as average_income_in_zone",
    ],
    5:   #SINGLE
            [
#    "constant",
#    "parcel.area",
#    "parcel.land_value",    
#    
    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_households,[parcel]) as households_in_zone",
#    "parcel:opus_core.func.disaggregate(parcel.area) as lot_area",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.employment_of_sector_retailent,[parcel]) as employment_of_sector_retailent_in_zone",             
#    "parcel:opus_core.func.disaggregate(az_smart.zone.number_of_businesses_of_sector_retailent,[parcel]) as businesses_of_sector_retailent_in_zone",             
    
    "parcel:opus_core.func.disaggregate(az_smart.zone.average_income, [parcel]) as average_income_in_zone",
    ],

}