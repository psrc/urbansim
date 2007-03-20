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
##|              14 | RETAIL/ENT   |      279 |
##|              16 | VACANT       |       20 |
##|              17 | VISITOR      |       12 |
##+-----------------+--------------+----------+

specification ={}
specification = {  
        1:   #APT
            [
    "constant",
    "building.year_built",
#    
    "building.bedrooms",
        
#    "building.building_sqft",
    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_households,[parcel]) as households_in_zone",
#    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
    
    "building:opus_core.func.disaggregate(sanfrancisco.zone.average_income, [parcel]) as average_income_in_zone",
#    

#    "building.stories",
#    "building.structure_value",    
    ],
    2:   #CONDO
            [
    "constant",
    "building.year_built",
##    
    "building.bedrooms",
#        
#    "building.building_sqft",
#    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_households,[parcel]) as households_in_zone",
    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
    
    "building:opus_core.func.disaggregate(sanfrancisco.zone.average_income, [parcel]) as average_income_in_zone",
##    
#
##    "building.stories",
##    "building.structure_value",    
    ],
    3:   #FLATS
            [
    "constant",
    "building.year_built",
##    
    "building.bedrooms",
#        
#    "building.building_sqft",
#    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_households,[parcel]) as households_in_zone",
    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
    
    "building:opus_core.func.disaggregate(sanfrancisco.zone.average_income, [parcel]) as average_income_in_zone",
#
##    "building.stories",
##    "building.structure_value",    
    ],
    5:   #SINGLE
            [
    "constant",
    "building.year_built",
#    
    "building.bedrooms",
#        
    "building.building_sqft",
#    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_households,[parcel]) as households_in_zone",
    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
    
    "building:opus_core.func.disaggregate(sanfrancisco.zone.average_income, [parcel]) as average_income_in_zone",

#
##    "building.stories",
##    "building.structure_value",    
    ],

    10:   #mixed residential
            [
    "constant",
    "building.year_built",
#    
    "building.bedrooms",
#        
    "building.building_sqft",
#    "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_households,[parcel]) as households_in_zone",
    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
#
##    "building.stories",
##    "building.structure_value",    
    ]

}            
