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
        3:   #commercial
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    "ln_land=ln(building.footprint_sqft)",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",

    ],

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
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp45tw=ln(building.disaggregate(psrc.zone.employment_within_45_minutes_travel_time_hbw_am_transit_walk))",
#    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    ],
    


    8:   #industrial
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    "ln_land=ln(building.footprint_sqft)",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
    ],

    10:   #Mixed Use
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    "ln_land=ln(building.footprint_sqft)",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
    ],


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
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp45tw=ln(building.disaggregate(psrc.zone.employment_within_45_minutes_travel_time_hbw_am_transit_walk))",
#    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    ],
    
    13:   #Office
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "lngcdacbd=ln(building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd))",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    "ln_land=ln(building.footprint_sqft)",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
    ],


    19:   #SINGLE family residential
            [
    "constant",
    "building.year_built",
#    "new=building.year_built>2000",
    "preww2=building.year_built<1945",
    "beds=building.number_of_bedrooms/building.residential_units",
    "sqft_bed=building.building_sqft/building.number_of_bedrooms",#    "baths=building.number_of_bathrooms",
    "lnsqft=ln(building.building_sqft/building.residential_units)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",        #    "lnsqft=ln(building.building_sqft)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "ln_parcel_sqft=ln(building.disaggregate(parcel.parcel_sqft))",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp20da=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lngcdacbd=ln(building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd))",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    ],

    20:   #Transportation Communications and Utilities
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    "ln_land=ln(building.footprint_sqft)",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
   ],


    21:   #Warehouse
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    "ln_land=ln(building.footprint_sqft)",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
    ],
        
    23:   #Vacant Land
        [
    "constant",
    "ln_parcel_sqft=ln(building.disaggregate(parcel.parcel_sqft))",
#    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp20da=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lngcdacbd=ln(building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd))",
#    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    ],
}            
