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
#    "building.year_built",
    "ln_bldgage=ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean))",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
    "ln_invfar=ln(parcel.parcel_sqft/parcel.aggregate(building.building_sqft))",
#    "building.stories",
    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "lnemp30da=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",

    ],

    10:   #industrial
            [
    "constant",
#    "building.year_built",
    "ln_bldgage=ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean))",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnemp30da=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],


    14:   #multi-family residential
            [
    "constant",
#    "yrblt10=building.year_built/10",
#    "new=parcel.aggregate(building.year_built>2000)>=1",
#    "preww2=parcel.aggregate(building.year_built<1945) >= 1",
#    "beds=parcel.aggregate(building.number_of_bedrooms)/parcel.aggregate(building.residential_units)",
    "lnbedsqft=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.number_of_bedrooms))",
#    "baths=building.number_of_bathrooms",
    "lnsqftunit=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.residential_units))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",        
#    "lnsqft=ln(building.building_sqft)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "lnlotsqft=ln(parcel.parcel_sqft)",
#    "lnlotgccbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(parcel.parcel_sqft)",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
#    "lnemp20da=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnempden=ln(parcel.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],


    15:   #condominium multi-family 
            [
    "constant",
#    "yrblt10=building.year_built/10",
#    "new=parcel.aggregate(building.year_built>2000)>=1",
#    "preww2=parcel.aggregate(building.year_built<1945) >= 1",
#    "beds=parcel.aggregate(building.number_of_bedrooms)/parcel.aggregate(building.residential_units)",
    "lnbedsqft=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.number_of_bedrooms))",
#    "baths=parcel.aggregate(building.number_of_bathrooms)",
    "lnsqftunit=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.residential_units))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",        
#    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "lnlotsqft=ln(parcel.parcel_sqft)",
#    "lnlotgccbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(parcel.parcel_sqft)",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
#    "lnemp20da=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnempden=ln(parcel.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],
    
    18:   #Office
            [
    "constant",
#    "building.year_built",
    "ln_bldgage=ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean))",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "far10=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft>10",
    "ln_invfar=ln(parcel.parcel_sqft/parcel.aggregate(building.building_sqft))",
#    "building.stories",
#    "hirise15=building.stories>15",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "lnempden=ln(parcel.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnemp30da=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],


    24:   #SINGLE family residential
            [
    "constant",
#    "yrblt10=building.year_built/10",
    "ln_bldgage=ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean))",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
#    "new=parcel.aggregate(building.year_built>2000)>=1",  #won't work (5/4/07)
    #"preww2=parcel.aggregate(building.year_built<1945) >= 1", #won't work
#    "bedrooms=parcel.aggregate(building.number_of_bedrooms)/parcel.aggregate(building.residential_units)",
    "lnbedsqft=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.number_of_bedrooms))",
#    "baths=building.number_of_bathrooms",
    "lnsqftunit=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.residential_units))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",        
#    "lnsqft=ln(building.building_sqft)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
    "lnlotsqft=ln(parcel.parcel_sqft)",
#    "lnlotgccbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(parcel.parcel_sqft)",
##    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
#    "lnemp20da=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnempden=ln(parcel.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],

    25:   #Transportation Communications and Utilities
            [
    "constant",
#    "building.year_built",
    "ln_bldgage=ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean))",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
    "ln_invfar=ln(parcel.parcel_sqft/parcel.aggregate(building.building_sqft))",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
    "lnemp30da=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
   ],


    26:   #Vacant Land
        [
    "constant",
    "lnlotsqft=ln(parcel.parcel_sqft)",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp20da=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
    "lnempden=ln(parcel.disaggregate(psrc.zone.number_of_jobs_per_acre))",
#    "in_ugb=parcel.is_inside_urban_growth_boundary",
#    "plan_1=parcel.plan_type_id==1",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],

    28:   #Warehouse
            [
    "constant",
#    "building.year_built",
    "ln_bldgage=ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean))",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
    "lnemp30da=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
#    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],    


#    10:   #Mixed Use
#            [
#    "constant",
##    "building.year_built",
#    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
##    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
##    "building.stories",
##    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
##    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
##    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
##    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
##    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
##    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
#    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
##    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
##    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
#    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
#    ],
    
}            
