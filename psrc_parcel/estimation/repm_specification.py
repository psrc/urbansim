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
#    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))",
#    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",

    ],

    4:   #multi-family condominium
            [
    "constant",
#    "yrblt10=building.year_built/10",
#    "new=building.year_built>2000",
#    "preww2=building.year_built<1945",
#    "beds=building.number_of_bedrooms/building.residential_units",
    "lnbedsqft=ln(building.building_sqft/building.number_of_bedrooms)",
#    "baths=building.number_of_bathrooms",
    "lnsqftunit=ln(building.building_sqft/building.residential_units)",
    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",        
#    "lnsqft=ln(building.building_sqft)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "lnlotsqft=ln(building.disaggregate(parcel.parcel_sqft))",
#    "lnlotgccbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(building.disaggregate(parcel.parcel_sqft))",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp20da=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnempden=ln(building.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    ],
    


    8:   #industrial
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
#    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
#    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(building.footprint_sqft)",
#    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
    ],

    10:   #Mixed Use
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
#    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
#    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(building.footprint_sqft)",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnemp10da=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
    ],


    12:   #multi-family residential
            [
    "constant",
#    "yrblt10=building.year_built/10",
#    "new=building.year_built>2000",
#    "preww2=building.year_built<1945",
    "beds=building.number_of_bedrooms/building.residential_units",
    "lnbedsqft=ln(building.building_sqft/building.number_of_bedrooms)",
#    "baths=building.number_of_bathrooms",
    "lnsqftunit=ln(building.building_sqft/building.residential_units)",
#    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",        
#    "lnsqft=ln(building.building_sqft)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "lnlotsqft=ln(building.disaggregate(parcel.parcel_sqft))",
#    "lnlotgccbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(building.disaggregate(parcel.parcel_sqft))",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp20da=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnempden=ln(building.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    ],
    
    13:   #Office
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
#    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "far10=building.building_sqft/building.disaggregate(parcel.parcel_sqft)>10",
#    "building.stories",
    "hirise15=building.stories>15",
    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=building.disaggregate(psrc.zone.population_per_acre)",
    "ln_land=ln(building.footprint_sqft)",
#    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
    ],


    19:   #SINGLE family residential
            [
    "constant",
    "yrblt10=building.year_built/10",
#    "new=building.year_built>2000",
    "preww2=building.year_built<1945",
#    "bedrooms=building.number_of_bedrooms/building.residential_units",
    "lnbedsqft=ln(building.building_sqft/building.number_of_bedrooms)",#    "baths=building.number_of_bathrooms",
    "lnsqftunit=ln(building.building_sqft/building.residential_units)",
#    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",        #    "lnsqft=ln(building.building_sqft)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "lnlotsqft=ln(building.disaggregate(parcel.parcel_sqft))",
#    "lnlotgccbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(building.disaggregate(parcel.parcel_sqft))",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp20da=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnempden=ln(building.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    ],

    20:   #Transportation Communications and Utilities
            [
    "constant",
    "building.year_built",
    "lnsqft=ln(building.building_sqft)",
#    "far=building.building_sqft/building.disaggregate(parcel.parcel_sqft)",
#    "building.stories",
#    "empden=building.disaggregate(psrc.zone.number_of_jobs_per_acre)",
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
#    "ln_land=ln(building.footprint_sqft)",
    "lnemp30da=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(building.footprint_sqft)",
    ],
        
    23:   #Vacant Land
        [
    "constant",
    "lnlotsqft=ln(building.disaggregate(parcel.parcel_sqft))",
    "lnemp10wa=ln(building.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnemp20da=ln(building.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(building.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "gcdacbd=building.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnempden=ln(building.disaggregate(psrc.zone.number_of_jobs_per_acre))",
#    "in_ugb=building.disaggregate(parcel.is_inside_urban_growth_boundary)",
#    "plan_1=building.disaggregate(parcel.plan_type_id)==1",
    ],
}            
