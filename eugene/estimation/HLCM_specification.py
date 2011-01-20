# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

#######
# In a command line, you can estimate using this command:
#  
# python urbansim/tools/start_estimation.py -c eugene.configs.baseline_estimation --model=household_location_choice_model -s eugene.estimation.HLCM_specification
#
# see 
# python urbansim/tools/start_estimation.py --help
# for other options
#######

specification = {}
#
# ############################# Residential ##############################
#
specification = {
        -2:   #submodel_id
            [
#            "lnhousing_cost = ln(urbansim.gridcell.housing_cost)",
            "urbansim.household_x_gridcell.cost_to_income_ratio",
#            "urbansim.household_x_gridcell.housing_affordability",
            "urbansim.household_x_gridcell.income_and_year_built",
#            "urbansim.household_x_gridcell.income_and_ln_residential_units",
#            "urbansim.household_x_gridcell.income_and_percent_residential",
            "urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_low_income",
            "urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_high_income",
            "urbansim.household_x_gridcell.young_household_in_high_density_residential",
            "urbansim.household_x_gridcell.young_household_in_mixed_use",
#            "urbansim.gridcell.is_near_highway",
            #"urbansim.gridcell.is_near_arterial",
#            "ln_bounded(urbansim.household_x_gridcell.income_less_housing_cost)",
#            "urbansim.gridcell.travel_time_to_CBD",
#            "urbansim.gridcell.acres_open_space_within_walking_distance",
#            "urbansim.household_x_gridcell.income_and_ln_improvement_value_per_unit",
#            "ltotal_resvalue_per_ru_wwd = ln(urbansim.gridcell.total_residential_value_per_residential_unit_within_walking_distance)",
#            "ltotal_impvalue_per_ru_wwd = ln(urbansim.gridcell.total_improvement_value_per_residential_unit_within_walking_distance)",
#            "urbansim.gridcell.ln_residential_units",
#            "urbansim.gridcell.ln_residential_units_within_walking_distance",\
            #"urbansim.gridcell.ln_service_sector_employment_within_walking_distance",\
            #"urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",\
            #"urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
            #"urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_high_income",\
            #"urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_low_income",\
            #"urbansim.household_x_gridcell.percent_mid_income_households_within_walking_distance_if_mid_income", \
            "urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_minority",\
            #"urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_not_minority",\
            "urbansim.household_x_gridcell.residential_units_when_household_has_children",\
#            "urbansim.household_x_gridcell.utility_for_transit_walk_0_cars",
#            "urbansim.gridcell.ln_home_access_to_employment_1",\
#            "urbansim.household_x_gridcell.same_household_age_in_faz",
            #"utility_for_transit_walk_0_cars",\
            #"utility_for_transit_walk_1_person"
            #"ln_access_from_residence_to_workplaces",\
            #"trip_weighted_average_utility_hbw_from_home_am_income_1",\
            #"trip_weighted_average_utility_hbw_from_home_am_income_2",\
            #"trip_weighted_average_utility_hbw_from_home_am_income_3",\
            #"trip_weighted_average_utility_hbw_from_home_am_income_4"\
            ]
    }