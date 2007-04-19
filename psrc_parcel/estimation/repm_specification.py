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
#        3:   #commercial
#            [
#    "constant",
#    "building.year_built",
##    
#    "building.bedrooms",
#        
##    "building.building_sqft",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
##    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
#    
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.average_income, [parcel]) as average_income_in_zone",
##    
#
##    "building.stories",
##    "building.structure_value",    
#    ],
#    8:   #industrial
#            [
#    "constant",
#    "building.year_built",
###    
#    "building.bedrooms",
##        
##    "building.building_sqft",
##    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.bus_travel_time_weighted_access_by_population,[parcel]) as bus_travel_time_weighted_access_by_population",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.bus_travel_time_weighted_access_to_employment,[parcel]) as bus_travel_time_weighted_access_to_employment",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_within_20_minutes_bus_travel_time,[parcel]) as employment_within_20_minutes_bus_travel_time",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_businesses_of_sector_cie,[parcel]) as businesses_of_sector_cie_in_zone",             
#    
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.average_income, [parcel]) as average_income_in_zone",
###    
##
###    "building.stories",
###    "building.structure_value",    
#    ],
    12:   #mulit-family residential
            [
    "constant",
    "building.year_built",
#    
    "building.number_of_bedrooms",
    "building.number_of_bathrooms",
    "building.stories",        
#        
    "building.building_sqft",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "parcel_sqft=building.disaggregate(parcel.parcel_sqft)",
    "gc_da_to_cbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd, intermediates=[parcel])",
    ],
    
    19:   #SINGLE family residential
            [
    "constant",
    "building.year_built",
#    
    "building.number_of_bedrooms",
    "building.number_of_bathrooms",
    "building.stories",        
#        
    "building.building_sqft",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "parcel_sqft=building.disaggregate(parcel.parcel_sqft)",
    "gc_da_to_cbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd, intermediates=[parcel])",
    ],
}            
