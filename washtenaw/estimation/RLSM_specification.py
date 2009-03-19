# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

specification = {}
#
# ############################# Residential ##############################  
#
specification = {
             -2:  # submodel id
    [
    "constant",
#            "ln(urbansim.gridcell.housing_cost)",
            "urbansim.gridcell.travel_time_to_CBD",
            "urbansim.gridcell.acres_open_space_within_walking_distance",
#            "urbansim.gridcell.ln_residential_units",
#            "urbansim.gridcell.ln_residential_units_within_walking_distance",\
#            "urbansim.gridcell.ln_service_sector_employment_within_walking_distance",\
#            "urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",\
#            "urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
            "urbansim.gridcell.ln_home_access_to_employment_1",\
#            "utility_for_transit_walk_0_cars",\
#            "young_household_in_mixed_use",\
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
