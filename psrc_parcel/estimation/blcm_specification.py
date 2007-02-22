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
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.hwy_travel_time_weighted_access_to_employment,[parcel]) as hwy_travel_time_weighted_access_to_employment",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_within_20_minutes_hwy_travel_time,[parcel]) as employment_within_20_minutes_hwy_travel_time",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_mips,[parcel]) as employment_of_sector_mips_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_mips,[parcel]) as businesses_of_sector_mips_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.average_income, [parcel]) as average_income_in_zone",
    "building.stories",
#    "building.structure_value",    
    ],

        8:   #MIPS
            [
    "building.year_built",
    "building.building_sqft",
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.hwy_travel_time_weighted_access_to_employment,[parcel]) as hwy_travel_time_weighted_access_to_employment",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_within_20_minutes_hwy_travel_time,[parcel]) as employment_within_20_minutes_hwy_travel_time",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_mips,[parcel]) as employment_of_sector_mips_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_mips,[parcel]) as businesses_of_sector_mips_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.average_income, [parcel]) as average_income_in_zone",
    "building.stories",
#    "building.structure_value",    
    ],

    13:   #PDR
            [
    "building.year_built",
    "building.building_sqft",
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.hwy_travel_time_weighted_access_to_employment,[parcel]) as hwy_travel_time_weighted_access_to_employment",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_within_20_minutes_hwy_travel_time,[parcel]) as employment_within_20_minutes_hwy_travel_time",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_mips,[parcel]) as employment_of_sector_mips_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_mips,[parcel]) as businesses_of_sector_mips_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.average_income, [parcel]) as average_income_in_zone",
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_pdr,[parcel]) as employment_of_sector_rpdr_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_pdr,[parcel]) as businesses_of_sector_pdr_in_zone",             
    "building.stories",
#    "building.structure_value",    
    ],

    14:   #RETAIL/ENT
            [
    "building.year_built",
    "building.building_sqft",
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.hwy_travel_time_weighted_access_to_employment,[parcel]) as hwy_travel_time_weighted_access_to_employment",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_within_20_minutes_hwy_travel_time,[parcel]) as employment_within_20_minutes_hwy_travel_time",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_mips,[parcel]) as employment_of_sector_mips_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_mips,[parcel]) as businesses_of_sector_mips_in_zone",             
    "building:opus_core.func.disaggregate(psrc_parcel.zone.average_income, [parcel]) as average_income_in_zone",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_retail/ent,[parcel]) as employment_of_sector_retail/ent_in_zone",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_retail/ent,[parcel]) as businesses_of_sector_retail/ent_in_zone",             
    "building.stories",
#    "building.structure_value",    
    ],
}            
