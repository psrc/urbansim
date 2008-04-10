
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

specification = {
        0:   #submodel_id
            [

#        ALTERNATIVE
#             "A_is_new_construction = (urbansim_parcel.building.age_masked < 2)",
#             "A_is_pre1945 = (urbansim_parcel.building.age_masked > 60)",
             "A_ln_sqft_per_unit = ln(psrc_parcel.building.sqft_per_unit)",
#             "A_ln_building_age = ln(urbansim_parcel.building.age_masked)",
#             "A_ln_land_area = ln(psrc_parcel.building.land_area)",
#             "A_ln_parcel_sf_per_unit = ln(urbansim_parcel.building.parcel_sqft_per_unit)",
#             "A_ln_price_per_sqft = ln(urbansim_parcel.building.unit_price)",
             "A_ln_price_per_unit = ln((urbansim_parcel.building.unit_price) * urbansim_parcel.building.building_sqft_per_unit)",
#             "A_ln_residential_units = ln(psrc_parcel.building.residential_units)",
#             "A_unit_price = urbansim_parcel.building.unit_price * urbansim_parcel.building.building_sqft_per_unit",
                          
#        NEIGHBOURHOOD
#             "B_average_household_size_within_walking_distance = building.disaggregate(psrc.parcel.average_household_size_within_walking_distance)",
#             "B_ln_average_zonal_income = ln(building.disaggregate(urbansim_parcel.zone.average_income))",
#             "B_ln_number_of_households = ln(building.disaggregate(urbansim_parcel.zone.number_of_households))",
#             "B_ln_retail_sector_employment_within_walking_distance = building.disaggregate(psrc.parcel.ln_retail_sector_employment_within_walking_distance)",
             "B_ln_zonal_emp_den = (ln(building.disaggregate(urbansim_parcel.zone.number_of_jobs_per_acre))).astype(float32)",
             "B_ln_zonal_pop_den = (ln(building.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)",
#             "B_number_of_high_income_households_within_walking_distance = building.disaggregate(psrc.parcel.number_of_high_income_households_within_walking_distance)",
#             "B_percent_high_income_households_within_walking_distance = building.disaggregate(psrc.parcel.percent_high_income_households_within_walking_distance)",
#             "B_percent_low_income_households_within_walking_distance = building.disaggregate(psrc.parcel.percent_low_income_households_within_walking_distance)",
#             "B_percent_med_income_households_within_walking_distance = building.disaggregate(psrc.parcel.percent_mid_income_households_within_walking_distance)",
             "B_percent_young_households_within_walking_distance = building.disaggregate(psrc.parcel.percent_young_households_within_walking_distance)",
#             "urbansim_parcel.household_x_building.ln_sampling_probability_for_bias_correction_mnl_vacant_residential_units",


#        HH & ALTERNATIVE INTERACTIONS
             "C_has_children_x_is_single_family_residential = (household.children > 0) * urbansim.building.is_single_family_residential",
#             "C_is_high_income_x_is_new_construction = urbansim.household.is_high_income * (urbansim_parcel.building.age_masked < 2)",
#             "C_is_high_income_x_is_pre1945 = urbansim.household.is_high_income * (urbansim_parcel.building.age_masked > 60)",             
#             "C_is_high_income_x_ln_average_income_within_walking_distance = urbansim.household.is_high_income * ln(building.disaggregate(psrc.parcel.average_income_within_walking_distance))",
             "C_is_high_income_x_ln_average_zonal_income = urbansim.household.is_high_income * ln(building.disaggregate(urbansim_parcel.zone.average_income))",
#             "C_is_high_income_x_ln_percent_high_income_households_within_walking_distance = urbansim.household.is_high_income * ln(building.disaggregate(psrc.parcel.percent_high_income_households_within_walking_distance))",
#             "C_is_high_income_x_percent_high_income_households_within_walking_distance = urbansim.household.is_high_income * building.disaggregate(psrc.parcel.percent_high_income_households_within_walking_distance)",
#             "C_is_high_income_x_ln_zonal_pop_den = urbansim.household.is_high_income * (ln(building.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)",
#             "C_is_low_income_x_is_condo_residential = urbansim.household.is_low_income * urbansim.building.is_condo_residential",
             "C_is_low_income_x_is_multi_family_residential = urbansim.household.is_low_income * urbansim.building.is_multi_family_residential",
#             "C_is_low_income_x_is_not_single_family_residential = urbansim.household.is_low_income * numpy.logical_not(urbansim.building.is_single_family_residential)",
#             "C_is_low_income_x_ln_zonal_pop_den = urbansim.household.is_low_income * (ln(building.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)",
             "C_is_single_person_x_is_not_single_family_residential = (household.persons < 2) * numpy.logical_not(urbansim.building.is_single_family_residential)",
             "C_ln_income_less_price_per_unit = ln_bounded(household.income - (urbansim_parcel.building.unit_price/10.))", # * urbansim_parcel.building.building_sqft_per_unit
#             "C_ln_income_x_is_new_construction = ln(household.income) * (urbansim_parcel.building.age_masked < 2)",
#             "C_ln_income_x_is_pre1945 = ln(household.income) * (urbansim_parcel.building.age_masked > 60)",
#             "C_ln_income_x_ln_average_income_within_walking_distance = ln(household.income) * ln(building.disaggregate(psrc.parcel.average_income_within_walking_distance))",
#             "C_ln_income_x_ln_average_zonal_income = ln(household.income) * ln(building.disaggregate(urbansim_parcel.zone.average_income))",
             "C_ln_income_x_ln_price_per_sqft = ln(household.income) * ln(urbansim_parcel.building.unit_price)",
#             "C_ln_income_x_ln_zonal_pop_den = ln(household.income) * (ln(building.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)",

#             "C_hh_size_x_ln_zonal_pop_den = household.persons * (ln(building.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)",
#             "C_has_children_x_ln_zonal_pop_den = (household.children > 0) * (ln(building.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)",
             
                          
#        ACCESSIBILITY
#             "D_ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone = ln(urbansim.building.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone)",
#             "D_ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk = ln(urbansim.building.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)",
#             "D_ln_generalized_cost_weighted_access_to_employment_hbw_am_drive_alone = ln(building.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_drive_alone))",
#             "D_ln_generalized_cost_weighted_access_to_employment_hbw_am_transit_walk = ln(building.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))",
#             "D_ln_trip_weighted_average_time_hbw_from_home_am_drive_alone = ln(building.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_drive_alone))",
#             "D_ln_trip_weighted_average_time_hbw_from_home_am_transit_walk = ln(building.disaggregate(psrc.zone.trip_weighted_average_time_hbw_from_home_am_transit_walk))",

            ],
          
    }
