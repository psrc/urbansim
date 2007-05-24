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

all_variables = [
    "hwy600 = psrc.parcel.distance_to_highway_in_gridcell<600",
    "hwy1000 = psrc.parcel.distance_to_highway_in_gridcell<1000",
    "hwy2000 = psrc.parcel.distance_to_highway_in_gridcell<2000",
    "art300 = psrc.parcel.distance_to_arterial_in_gridcell<300",
    "art600 = psrc.parcel.distance_to_arterial_in_gridcell<600",
    "ln_bldgage=ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean))",
    "lnsqft=ln(parcel.aggregate(psrc_parcel.building.building_sqft))",
    "lnsqftunit=ln(parcel.aggregate(psrc_parcel.building.building_sqft)/parcel.aggregate(building.residential_units))",
    "lnlotsqft=ln(parcel.parcel_sqft)",
    "lnlotsqftunit=ln(parcel.parcel_sqft/parcel.aggregate(building.residential_units))",
    "ln_invfar=ln(parcel.parcel_sqft/parcel.aggregate(psrc_parcel.building.building_sqft))",
    "lngcdacbd=ln(parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd))",
    "lnemp30da=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp20da=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "lnemp20tw=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))",
    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    "lnempden=ln(parcel.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    "lnpopden=ln(parcel.disaggregate(psrc.zone.population_per_acre))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "inugb = parcel.is_inside_urban_growth_boundary*1",
    "hbwavgtmda = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
    "plan_3=parcel.plan_type_id==3",
    "plan_4=parcel.plan_type_id==4",
    "plan_5=parcel.plan_type_id==5",
    "plan_6=parcel.plan_type_id==6",
    "plan_7=parcel.plan_type_id==7",
    "plan_8=parcel.plan_type_id==8",
    "plan_9=parcel.plan_type_id==9",
    "plan_10=parcel.plan_type_id==10",
    "plan_11=parcel.plan_type_id==11",
    "plan_12=parcel.plan_type_id==12",
    "plan_13=parcel.plan_type_id==13",
    "plan_14=parcel.plan_type_id==14",
    "plan_15=parcel.plan_type_id==15",
    "plan_16=parcel.plan_type_id==16",
    "plan_19=parcel.plan_type_id==19",
    "plan_20=parcel.plan_type_id==20",           
                 ]
variables_for_development_project_proposal = {
      'ln_bldgage' : 'ln(psrc_parcel.development_project_proposal.building_age)',
      'lnsqft': 'ln(psrc_parcel.development_project_proposal.units_proposed)',
      "lnsqftunit": 'ln(psrc_parcel.development_project_proposal.units_proposed)', # wrong
      "lnlotsqftunit": "ln(development_project_proposal.aggregate(parcel.parcel_sqft)/psrc_parcel.development_project_proposal.units_proposed)", # wrong
      "ln_invfar": "ln(development_project_proposal.aggregate(parcel.parcel_sqft)/psrc_parcel.development_project_proposal.units_proposed)",
                                              }
specification ={}
specification = {
       "_definition_": all_variables,
       
        1:   #commercial
            [
    "constant",
#    "building.year_built",
    "hwy600",
    "art600",
    "ln_bldgage",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
    "ln_invfar",
#    "building.stories",
#    "lnempden=ln(parcel.disaggregate(psrc.zone.number_of_jobs_per_acre))",
    "lngcdacbd",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_walk))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
    "lnemp30da",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc",
    "lnempden",
    "lnpopden",
#    "plan_1=parcel.plan_type_id==1",

    ],

    2:   #industrial
            [
    "constant",
#    "building.year_built",
#    "hwy1000 = psrc.parcel.distance_to_highway_in_gridcell<1000",
#    "art600 = psrc.parcel.distance_to_arterial_in_gridcell<600",
    "ln_bldgage",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft",
    "ln_invfar",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "lngcdacbd",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnemp30da",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
#    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    "lnempden",
    "lnpopden",
#    "plan_3=parcel.plan_type_id==3",

    ],


    3:   #multi-family residential
            [
    "constant",
    "hwy600",
    "art300",
#    "ln_bldgage=ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean))",
#    "bldgage=parcel.aggregate(psrc_parcel.building.age_masked, function=mean)",
#    "yrblt10=building.year_built/10",
#    "new=parcel.aggregate(building.year_built>2000)>=1",
#    "pre1940=parcel.aggregate(building.year_built<1940)>=1",
#    "beds=parcel.aggregate(building.number_of_bedrooms)/parcel.aggregate(building.residential_units)",
#    "lnbedsqft=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.number_of_bedrooms))",
#    "baths=building.number_of_bathrooms",
    "lnsqftunit",
    "lnlotsqftunit",
#    "ln_invfar=ln(parcel.parcel_sqft/parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",        
#    "lnsqft=ln(building.building_sqft)",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "lnlotsqft=ln(parcel.parcel_sqft)",
#    "lnlotgccbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(parcel.parcel_sqft)",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
#    "lnemp20da=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
    "lnavginc",
    ],


    4:   #condominium multi-family 
            [
    "constant",
    "hwy600",
    "art600",
    "ln_bldgage",
#    "yrblt10=building.year_built/10",
#    "new=parcel.aggregate(building.year_built>2000)>=1",
#    "preww2=parcel.aggregate(building.year_built<1945) >= 1",
#    "beds=parcel.aggregate(building.number_of_bedrooms)/parcel.aggregate(building.residential_units)",
#    "lnbedsqft=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.number_of_bedrooms))",
#    "baths=parcel.aggregate(building.number_of_bathrooms)",
    "lnsqftunit",
#    "ln_invfar=ln(parcel.parcel_sqft/parcel.aggregate(building.building_sqft))",
    "lnlotsqftunit",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",        
#    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "lnlotsqft=ln(parcel.parcel_sqft)",
#    "lnlotgccbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(parcel.parcel_sqft)",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
#    "trip_wt_avg_time_hbw_drive_alone = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
#    "lnemp20da=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp20tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "lnavginc",
    ],

    5:   #Mixed Commercial/Industrial
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(parcel.aggregate(psrc_parcel.building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],

    6:   #Mixed Commercial/Office
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ], 

    7:   #Mixed Commercial/Residential
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ], 

#    8:   #Mixed Commercial/Warehouse
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

    9:   #Mixed Industrial/Warehouse
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ], 

    10:   #Mixed Office/Industrial
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ], 

    11:   #Mixed Office/Residential
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ], 

    12:   #Mixed Office/Warehouse
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ], 

    13:   #Mixed Warehouse/Residential
            [
    "constant",
#    "building.year_built",
    "lnsqft=ln(parcel.aggregate(building.building_sqft))",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
#    "gcdacbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
#    "popden=parcel.disaggregate(psrc.zone.population_per_acre)",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp10da=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc=ln(parcel.disaggregate(urbansim.zone.average_income))",
    ],    

    14:   #Office
            [
    "constant",
#    "inugb = parcel.is_inside_urban_growth_boundary*1",
    "hwy1000",
#    "art300 = psrc.parcel.distance_to_arterial_in_gridcell<300",
#    "building.year_built",
    "ln_bldgage",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "far10=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft>10",
    "ln_invfar",
#    "building.stories",
#    "hirise15=building.stories>15",
#    "empden=parcel.disaggregate(psrc.zone.number_of_jobs_per_acre)",
    "lnempden",
    "lngcdacbd",
    "lnretempwa",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
    "lnpopden",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnemp30da=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))",
    "lnemp30tw",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc",
    ],


#    15:   #SINGLE family residential
#            [
#    "constant",
#    "inugb",
##    "pcthighinc = psrc.parcel.number_of_high_income_households_within_walking_distance / psrc.parcel.number_of_households_within_walking_distance",
#    "hwy600",
#    "art600",
##    "yrblt10=building.year_built/10",
#    "ln_bldgage",
##    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
##    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
##    "new=parcel.aggregate(building.year_built>2000)>=1",  #won't work (5/4/07)
#    #"preww2=parcel.aggregate(building.year_built<1945) >= 1", #won't work
##    "bedrooms=parcel.aggregate(building.number_of_bedrooms)/parcel.aggregate(building.residential_units)",
##    "lnbedsqft=ln(parcel.aggregate(building.building_sqft)/parcel.aggregate(building.number_of_bedrooms))",
##    "baths=building.number_of_bathrooms",
#    "lnsqftunit",
##    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
##    "building.stories",        
##    "lnsqft=ln(building.building_sqft)",
##    "building:opus_core.func.disaggregate(psrc_parcel.zone.number_of_households,[parcel]) as households_in_zone",
#    "lnlotsqft",
##    "lnlotgccbd=parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd)*ln(parcel.parcel_sqft)",
#    "lnemp10wa",
##    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
##    "lnemp20da=ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))",
#    "lnemp30tw",
#    "lngcdacbd",
#    "hbwavgtmda",
#    "lnempden",
#    "lnpopden",
#    "lnavginc",
#    ],

    17:   #Transportation Communications and Utilities
            [
    "constant",
    "hwy1000",
    "art600",
#    "building.year_built",
    "ln_bldgage",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft",
    "ln_invfar",
#    "building.stories",
    "lnempden",
    "lngcdacbd",
#    "lnemp30wa=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_walk))",
    "lnpopden",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
    "lnemp30da",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc",
   ],


    21:   #Vacant Land (Developable)
        [
    "constant",
    "inugb",
    "hwy1000",
    "art600",
    "lnlotsqft",
#    "lnemp10wa=ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))",
#    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "lnemp20da",
    "lnemp30tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
#    "in_ugb=parcel.is_inside_urban_growth_boundary",
#    "plan_1=parcel.plan_type_id==1",
#    "plan_2=parcel.plan_type_id==2",
    "plan_3",
    "plan_4",
#    "plan_5=parcel.plan_type_id==5",
#    "plan_6=parcel.plan_type_id==6",
#    "plan_7=parcel.plan_type_id==7",
#    "plan_8=parcel.plan_type_id==8",
    "plan_9",
#    "plan_10=parcel.plan_type_id==10",
    "plan_11",
#    "plan_12=parcel.plan_type_id==12",
    "plan_13",
#    "plan_14=parcel.plan_type_id==14",
#    "plan_15=parcel.plan_type_id==15",
#    "plan_16=parcel.plan_type_id==16",
#    "plan_19=parcel.plan_type_id==19",
    "plan_20",
    "lnavginc",
    ],

    18:   #Warehouse
            [
    "constant",
#    "inugb = parcel.is_inside_urban_growth_boundary*1",
    "hwy2000",
    "art600",
#    "building.year_built",
    "ln_bldgage",
#    "ln_bldgage2=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**2",
#    "ln_bldgage3=(ln(parcel.aggregate(psrc_parcel.building.age_masked, function=mean)))**3",
    "lnsqft",
    "ln_invfar",
#    "far=parcel.aggregate(building.building_sqft)/parcel.parcel_sqft",
#    "building.stories",
    "lnempden",
    "lngcdacbd",
    "lnpopden",
#    "ln_land=ln(parcel.aggregate(building.footprint_sqft))",
    "lnemp20da",
#    "land_access=ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))*ln(parcel.aggregate(building.footprint_sqft))",
    "lnavginc",
    ],    
}            
