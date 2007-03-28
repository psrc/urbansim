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
specification = {  
        7:   #CIE
            [
    "building.year_built",
    "building.building_sqft",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "lot_area=building.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "employment_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_cie,intermediates=[parcel])",             
    "businesses_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_cie,intermediates=[parcel])",             
    "employment_of_sector_mips_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_mips,intermediates=[parcel])",             
    "businesses_of_sector_mips_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_mips,intermediates=[parcel])",             
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    "building.stories",
#    "building.structure_value",    
    ],

        8:   #MIPS
            [
    "building.year_built",
    "building.building_sqft",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "lot_area=building.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",
    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "employment_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_cie,intermediates=[parcel])",             
    "businesses_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_cie,intermediates=[parcel])",             
    "employment_of_sector_mips_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_mips,intermediates=[parcel])",             
    "businesses_of_sector_mips_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_mips,intermediates=[parcel])",             
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    "building.stories",
#    "building.structure_value",    
    ],

    13:   #PDR
            [
    "building.year_built",
    "building.building_sqft",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "lot_area=building.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "employment_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_cie,intermediates=[parcel])",             
    "businesses_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_cie,intermediates=[parcel])",             
    "employment_of_sector_mips_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_mips,intermediates=[parcel])",             
    "businesses_of_sector_mips_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_mips,intermediates=[parcel])",             
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
    "employment_of_sector_rpdr_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_pdr,intermediates=[parcel])",             
    "businesses_of_sector_pdr_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_pdr,intermediates=[parcel])",             
    "building.stories",
#    "building.structure_value",    
    ],

    14:   #RETAIL/ENT
            [
    "building.year_built",
    "building.building_sqft",
    "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])",
    "lot_area=building.disaggregate(parcel.area)",             
    "bus_travel_time_weighted_access_by_population=building.disaggregate(sanfrancisco.zone.bus_travel_time_weighted_access_by_population,intermediates=[parcel])",             
    "hwy_travel_time_weighted_access_to_employment=building.disaggregate(sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment,intermediates=[parcel])",             
    "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])",             
    "employment_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_cie,intermediates=[parcel])",             
    "businesses_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_cie,intermediates=[parcel])",             
    "employment_of_sector_mips_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_mips,intermediates=[parcel])",             
    "businesses_of_sector_mips_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_mips,intermediates=[parcel])",             
    "average_income_in_zone=building.disaggregate(sanfrancisco.zone.average_income, intermediates=[parcel])",
#    "employment_of_sector_retail/ent_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_retail/ent,intermediates=[parcel])",             
#    "businesses_of_sector_retail/ent_in_zone=building.disaggregate(sanfrancisco.zone.number_of_businesses_of_sector_retail/ent,intermediates=[parcel])",             
    "building.stories",
#    "building.structure_value",    
    ],
}            
