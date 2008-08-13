#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
             -2:  # submodel id
    [
    "constant",

#            "ln(urbansim.gridcell.housing_cost)",
#            "urbansim.gridcell.travel_time_to_CBD",
#            "urbansim.gridcell.acres_open_space_within_walking_distance",
            "urbansim.gridcell.ln_residential_units",
            "ln_bounded(urbansim.gridcell.non_residential_sqft)",
#            "urbansim.gridcell.ln_residential_units_within_walking_distance",\
#            "urbansim.gridcell.ln_service_sector_employment_within_walking_distance",\
#            "urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",\
#            "urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
#            "urbansim.gridcell.ln_home_access_to_employment_1",\
#            "utility_for_transit_walk_0_cars",\
#            "young_household_in_mixed_use",\
#            "utility_for_transit_walk_1_person"
#            "ln_access_from_residence_to_workplaces",\
#            "trip_weighted_average_utility_hbw_from_home_am_income_1",\
#            "trip_weighted_average_utility_hbw_from_home_am_income_2",\
#            "trip_weighted_average_utility_hbw_from_home_am_income_3",\
#            "trip_weighted_average_utility_hbw_from_home_am_income_4"\
    ]
}
