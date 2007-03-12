#
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

specification = {}
#
# ############################# Residential ##############################
#
specification = {
        -2:   #submodel_id
            [
            "lhousing_cost = ln(urbansim.gridcell.housing_cost)",
#            "urbansim.household_x_gridcell.cost_to_income_ratio",
             "urbansim.household_x_gridcell.housing_affordability",
             "urbansim.household_x_gridcell.income_and_year_built",
             "urbansim.household_x_gridcell.income_and_ln_residential_units",
             "urbansim.household_x_gridcell.income_and_percent_residential",
            "urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_low_income",
            "urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_high_income",
            "urbansim.household_x_gridcell.young_household_in_high_density_residential",
            "urbansim.household_x_gridcell.young_household_in_mixed_use",
#           "urbansim.gridcell.is_near_highway",
#            "urbansim.gridcell.is_near_arterial",
#            "ln_bounded(urbansim.household_x_gridcell.income_less_housing_cost)",
#            "urbansim.gridcell.travel_time_to_CBD",
#            "urbansim.gridcell.acres_open_space_within_walking_distance",
            "urbansim.household_x_gridcell.income_and_ln_improvement_value_per_unit",
            "ltotal_resvalue_per_ru_wwd = ln(urbansim.gridcell.total_residential_value_per_residential_unit_within_walking_distance)",
            "ltotal_impvalue_per_ru_wwd = ln(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)",
#            "urbansim.gridcell.ln_residential_units",
            "urbansim.gridcell.ln_residential_units_within_walking_distance",\
#            "urbansim.gridcell.ln_service_sector_employment_within_walking_distance",\
#            "urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",\
#            "urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
#            "psrc.household_x_gridcell.ln_retail_sector_employment_within_walking_distance_if_has_less_cars_than_workers",
            "urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_high_income",
            "urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_low_income",
            "urbansim.household_x_gridcell.percent_mid_income_households_within_walking_distance_if_mid_income", 
            "urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_minority",
            "urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_not_minority",
            "urbansim.household_x_gridcell.residential_units_when_household_has_children",
#            "urbansim.household_x_gridcell.utility_for_transit_walk_0_cars",
            "urbansim.gridcell.ln_home_access_to_employment_1",\
#            "urbansim.household_x_gridcell.same_household_age_in_faz",
#            "utility_for_transit_walk_0_cars",\
#            "utility_for_transit_walk_1_person"
#            "ln_access_from_residence_to_workplaces",\
#            "trip_weighted_average_utility_hbw_from_home_am_income_1",\
#            "trip_weighted_average_utility_hbw_from_home_am_income_2",\
#            "trip_weighted_average_utility_hbw_from_home_am_income_3",\
#            "trip_weighted_average_utility_hbw_from_home_am_income_4"\
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone",
#             "psrc.household_x_gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk_if_has_less_cars_than_workers",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk**2",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone**2"
            ]
    }