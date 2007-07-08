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
    "ln_bldgage=(ln(parcel.aggregate(urbansim_parcel.building.age_masked, function=mean))).astype(float32)",
    "lnsqft=(ln(parcel.aggregate(urbansim_parcel.building.building_sqft))).astype(float32)",
    "lnsqftunit=(ln(parcel.aggregate(urbansim_parcel.building.building_sqft)/parcel.aggregate(building.residential_units))).astype(float32)",
    "lnlotsqft=(ln(parcel.parcel_sqft)).astype(float32)",
    "lnunits=(ln(parcel.aggregate(building.residential_units))).astype(float32)",
    "lnlotsqftunit=(ln(parcel.parcel_sqft/parcel.aggregate(building.residential_units))).astype(float32)",
    "ln_invfar=(ln(parcel.parcel_sqft/parcel.aggregate(urbansim_parcel.building.building_sqft))).astype(float32)",
    "lngcdacbd=(ln(parcel.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_cbd))).astype(float32)",
    "lnemp30da=(ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone))).astype(float32)",
    "lnemp20da=(ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))).astype(float32)",
    "lnemp10da=(ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_drive_alone))).astype(float32)",
    "lnemp30tw=(ln(parcel.disaggregate(psrc.zone.employment_within_30_minutes_travel_time_hbw_am_transit_walk))).astype(float32)",
    "lnemp20tw=(ln(parcel.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))).astype(float32)",
    "lnemp10wa=(ln(parcel.disaggregate(psrc.zone.employment_within_10_minutes_travel_time_hbw_am_walk))).astype(float32)",
    "lnavginc=(ln(parcel.disaggregate(urbansim.zone.average_income))).astype(float32)",
    "lnempden=(ln(parcel.disaggregate(urbansim_parcel.zone.number_of_jobs_per_acre))).astype(float32)",
#    "lnempden=ln(parcel.disaggregate(zone.number_of_agents(job)/(zone.aggregate(parcel.parcel_sqft) / 43560.0)))",
    "lnpopden=(ln(parcel.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)",
#    "lnpopden=ln(parcel.disaggregate(zone.aggregate(household.persons)/(zone.aggregate(parcel.parcel_sqft) / 43560.0)))",
#    "lnretempwa=ln(psrc.parcel.retail_sector_employment_within_walking_distance)",
    "inugb = parcel.is_inside_urban_growth_boundary*1",
    "hbwavgtmda = parcel.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone)",
    "plan_3=parcel.plan_type_id==3",
    "plan_4=parcel.plan_type_id==4",
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
    "plan_18=parcel.plan_type_id==18",
    "plan_19=parcel.plan_type_id==19",
    "plan_20=parcel.plan_type_id==20",
    "is_pre_1940 = parcel.aggregate(building.year_built,function=mean) < 1940",
                 ]
variables_for_development_project_proposal = {
      'ln_bldgage' : '(ln(urbansim_parcel.development_project_proposal.building_age)).astype(float32)',
      'lnsqft': '(ln(urbansim_parcel.development_project_proposal.building_sqft)).astype(float32)',
      "lnsqftunit": '(ln(urbansim_parcel.development_project_proposal.building_sqft/urbansim_parcel.development_project_proposal.units_proposed)).astype(float32)',
      "lnlotsqftunit": "(ln(development_project_proposal.aggregate(parcel.parcel_sqft)/urbansim_parcel.development_project_proposal.units_proposed)).astype(float32)",
      "ln_invfar": "(ln(development_project_proposal.aggregate(parcel.parcel_sqft)/urbansim_parcel.development_project_proposal.building_sqft)).astype(float32)",
                                              }
specification ={}
specification = {
       "_definition_": all_variables,
       
        1:   #Agriculture
            [
    "constant",
    "ln_bldgage",
    "lnsqft",
    "ln_invfar",
    "lngcdacbd",
    "lnemp30da",
    "lnavginc",
    "lnempden",
    "lnpopden",
    ],

    2:   #Civil and Quasi-Public
            [
    "constant",
    "ln_bldgage",
    "ln_invfar",
    "lnsqft",
    "lngcdacbd",
    "lnemp30da",
    "lnempden",
    "lnpopden",

    ],


    3:   #Commercial
            [
    "constant",
    "ln_bldgage",
    "lnsqft",
    "lnemp30da",
    "lnemp30tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
    "lnavginc",
    ],



    7:   #Government
            [
    "constant",
    "lnsqft",
    "lnemp10da",
    "lnavginc",
    ], 

#    8:   #Group Quarters
#            [
#    "constant",
#    ], 

    9:   #Hospital, Convalescent Center
            [
    "constant",
    "lnsqft",
    "lnemp10da",
    "lnavginc",
    ], 

    10:   #Industrial
            [
    "constant",
    "lnsqft",
    "lnemp10da",
    "lnavginc",
    ], 

    11:   #Military
            [
#   "constant",
    ], 

    12:   #Mining
            [
    "constant",
    "lnsqft",
    "lnemp10da",
    "lnavginc",
    ], 

    13:   #Mobile Home Park
            [
    "constant",
    "lnsqft",
    "lnemp10da",
    "lnavginc",
    "lnunits",
    ],    

    14:   #Multi-Family Residential (Apartment)
            [
    "constant",
    "ln_bldgage",
    "lnsqft",
    "ln_invfar",
    "lnempden",
    "lngcdacbd",
    "lnpopden",
    "lnemp30tw",
    "lnavginc",
    "lnunits",
    ],


    15:   #Condominium Residential
            [
    "constant",
    "inugb",
    "ln_bldgage",
    "lnsqftunit",
    "lnlotsqft",
    "lnemp10wa",
    "lnemp30tw",
    "lngcdacbd",
    "hbwavgtmda",
    "lnempden",
    "lnpopden",
    "lnavginc",
    "lnunits",
    ],

    18:   #Office
            [
    "constant",
    "ln_bldgage",
    "lnsqft",
    "ln_invfar",
    "lnempden",
    "lngcdacbd",
    "lnpopden",
    "lnemp30da",
    "lnavginc",
   ],

    19:   #Park and Open Space
            [
    "constant",
    "ln_bldgage",
    "lnsqft",
    "ln_invfar",
    "lnempden",
    "lngcdacbd",
    "lnpopden",
    "lnemp20da",
    "lnavginc",
    ],  
    
    20:   #Parking
        [
    "constant",
    "lnlotsqft",
    "lnemp20da",
    "lnemp30tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
    "lnavginc",
    ],


    24:   #Single Family Residential
            [
    "constant",
    "ln_bldgage",
    "lnsqftunit",
    "lnlotsqftunit",
    "lnemp20da",
    "lnemp20tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
    "lnavginc",
    ],

    25:   #Transportation, Communication, Public Utilities
            [
    "constant",
    "lnsqft",
    "lnemp20da",
    "lnemp20tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
    "lnavginc",
    ],

    26:   #Vacant Developable
            [
    "constant",
#    "lnemp30da",
#    "lnemp20tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
    "lnavginc",
    "inugb",
    "plan_3",
    "plan_8",
    "plan_11",
    "plan_13",
    "plan_14",
    "plan_15",
    "plan_18",
    "plan_20",    
    ], 
  
 #   27:   #Vacant Undevelopable
 #          [
 #   "constant",
 #   "lnsqft",
 #   "lnemp20da",
 #   "lnemp20tw",
 #   "lngcdacbd",
 #   "lnempden",
 #   "lnpopden",
 #   "lnavginc",
 #   ],


    28:   #Warehousing
            [
    "constant",
    "lnsqft",
    "lnemp20da",
    "lnemp20tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
    "lnavginc",
    ],

    30:   #Mixed Use
            [
    "constant",
    "lnsqft",
    "lnemp20da",
    "lnemp20tw",
    "lngcdacbd",
    "lnempden",
    "lnpopden",
    "lnavginc",
    "lnunits",
    ],
}            
