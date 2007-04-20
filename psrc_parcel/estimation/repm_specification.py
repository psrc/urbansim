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

    4:   #multi-family condominium
            [
    "constant",
    "building.year_built",
    "beds=building.number_of_bedrooms/building.residential_units",
    "sqft_bed=building.building_sqft/building.number_of_bedrooms",
#    "baths=building.number_of_bathrooms",
#    "building.stories",        
    "lnsqft=ln(building.building_sqft/building.residential_units)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
    "gc_da_to_cbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp45tw=ln(building.disaggregate(psrc.zone.employment_within_45_minutes_travel_time_hbw_am_transit_walk))",
#    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    ],
    


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
    12:   #multi-family residential
            [
    "constant",
    "building.year_built",    "beds=building.number_of_bedrooms/building.residential_units",
    "sqft_bed=building.building_sqft/building.number_of_bedrooms",
#    "baths=building.number_of_bathrooms",
#    "building.stories",        
    "lnsqft=ln(building.building_sqft/building.residential_units)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
    "gc_da_to_cbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp45tw=ln(building.disaggregate(psrc.zone.employment_within_45_minutes_travel_time_hbw_am_transit_walk))",
#    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    ],
    
    19:   #SINGLE family residential
            [
    "constant",
    "building.year_built",
    "new=building.year_built>2000",
    "preww2=building.year_built<1945",
    "beds=building.number_of_bedrooms/building.residential_units",
    "sqft_bed=building.building_sqft/building.number_of_bedrooms",#    "baths=building.number_of_bathrooms",
    "lnsqft=ln(building.building_sqft/building.residential_units)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",        #    "lnsqft=ln(building.building_sqft)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "ln_parcel_sqft=ln(building.disaggregate(parcel.parcel_sqft))",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp40da=ln(building.disaggregate(psrc.zone.employment_within_40_minutes_travel_time_hbw_am_drive_alone))",
    "lngcdacbd=ln(building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd))",
    ],
}            
