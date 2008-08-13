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

specification ={
         0: #number of non-home-based workers           
            [
#            "ln(urbansim.gridcell.housing_cost)",
            ("urbansim.household_x_gridcell.cost_to_income_ratio", "RCI"),
            ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#            "urbansim.household_x_gridcell.ln_income_less_housing_cost",
#            "urbansim.gridcell.travel_time_to_CBD",
#            "urbansim.gridcell.acres_open_space_within_walking_distance",
            ("urbansim.household_x_gridcell.income_and_ln_improvement_value_per_unit","IIMPPU"), 
            ("urbansim.gridcell.ln_residential_units","LDU"),
#            ("urbansim.gridcell.ln_residential_units_within_walking_distance","LUW"),
#            "urbansim.gridcell.ln_service_sector_employment_within_walking_distance",
#            "urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",
#            "urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
            ("psrc.household_x_gridcell.ln_retail_sector_employment_within_walking_distance_if_has_less_cars_than_workers","LRWCW"),
            ("urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_high_income","HIHIW"),
            ("urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_low_income","LILIW"),
            ("urbansim.household_x_gridcell.percent_mid_income_households_within_walking_distance_if_mid_income", "MIMIW"),
            ("urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_minority","MPMW"),
            ("urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_not_minority","NMPMW"),
            ("urbansim.household_x_gridcell.residential_units_when_household_has_children","UCH"),
#            ("urbansim.household_x_gridcell.young_household_in_high_density_residential","YHHD"),
##            ("gridcell.disaggregate(psrc.zone.ln_travel_time_weighted_access_to_employment_hbw_am_drive_alone)","GWAEDA"),            
            ('LNE20MDA = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone))','LNE30MDA'),
            ('LNE20MTW = ln(gridcell.disaggregate(psrc.zone.employment_within_20_minutes_travel_time_hbw_am_transit_walk))','LNE30MTW'),
#            ("generalized_cost_weighted_access_to_employment_hbw_am_transit_walk = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))", 'GWAETW'),
            #("ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))", 'GWAETW'),
#            "urbansim.household_x_gridcell.same_household_age_in_faz",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone",
#             "psrc.household_x_gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk_if_has_less_cars_than_workers",
#             "squared(psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
#             "squared(psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone)"

#           ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
             ],
         1: #number of non-home-based workers           
            [
#            "ln(urbansim.gridcell.housing_cost)",
            ("psrc.household_x_gridcell.worker1_travel_time_hbw_am_drive_alone_from_home_to_work","TT_HWDA"),
            ("psrc.household_x_gridcell.worker1_am_total_transit_time_walk_from_home_to_work","TT_HWTW"),
            ("urbansim.household_x_gridcell.cost_to_income_ratio", "RCI"),
            ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#            "urbansim.household_x_gridcell.ln_income_less_housing_cost",
#            "urbansim.gridcell.travel_time_to_CBD",
#            "urbansim.gridcell.acres_open_space_within_walking_distance",
            ("urbansim.household_x_gridcell.income_and_ln_improvement_value_per_unit","IIMPPU"), 
            ("urbansim.gridcell.ln_residential_units","LDU"),
#            ("urbansim.gridcell.ln_residential_units_within_walking_distance","LUW"),
#            "urbansim.gridcell.ln_service_sector_employment_within_walking_distance",
#            "urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",
#            "urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
            ("psrc.household_x_gridcell.ln_retail_sector_employment_within_walking_distance_if_has_less_cars_than_workers","LRWCW"),
            ("urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_high_income","HIHIW"),
            ("urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_low_income","LILIW"),
            ("urbansim.household_x_gridcell.percent_mid_income_households_within_walking_distance_if_mid_income", "MIMIW"),
            ("urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_minority","MPMW"),
            ("urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_not_minority","NMPMW"),
            ("urbansim.household_x_gridcell.residential_units_when_household_has_children","UCH"),
#            ("urbansim.household_x_gridcell.young_household_in_high_density_residential","YHHD"),
#            ("gridcell.disaggregate(psrc.zone.ln_travel_time_weighted_access_to_employment_hbw_am_drive_alone)","GWAEDA"),            
#            ("generalized_cost_weighted_access_to_employment_hbw_am_transit_walk = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))", 'GWAETW'),
            #("ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))", 'GWAETW'),
#            "urbansim.household_x_gridcell.same_household_age_in_faz",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone",
#             "psrc.household_x_gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk_if_has_less_cars_than_workers",
#             "squared(psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
#             "squared(psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone)"

#           ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
             ],

         2: #number of non-home-based workers           
            [
#            "ln(urbansim.gridcell.housing_cost)",
            ("psrc.household_x_gridcell.worker1_travel_time_hbw_am_drive_alone_from_home_to_work","TT_HWDA1"),
            ("psrc.household_x_gridcell.worker1_am_total_transit_time_walk_from_home_to_work","TT_HWTW"),
            ("psrc.household_x_gridcell.worker2_travel_time_hbw_am_drive_alone_from_home_to_work","TT_HWDA2"),
            ("psrc.household_x_gridcell.worker2_am_total_transit_time_walk_from_home_to_work","TT_HWTW2"),
            ("urbansim.household_x_gridcell.cost_to_income_ratio", "RCI"),
            ("urbansim.gridcell.percent_residential_within_walking_distance","PRW"),
#            "urbansim.household_x_gridcell.ln_income_less_housing_cost",
#            "urbansim.gridcell.travel_time_to_CBD",
#            "urbansim.gridcell.acres_open_space_within_walking_distance",
            ("urbansim.household_x_gridcell.income_and_ln_improvement_value_per_unit","IIMPPU"), 
            ("urbansim.gridcell.ln_residential_units","LDU"),
#            ("urbansim.gridcell.ln_residential_units_within_walking_distance","LUW"),
#            "urbansim.gridcell.ln_service_sector_employment_within_walking_distance",
#            "urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",
#            "urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
            ("psrc.household_x_gridcell.ln_retail_sector_employment_within_walking_distance_if_has_less_cars_than_workers","LRWCW"),
            ("urbansim.household_x_gridcell.percent_high_income_households_within_walking_distance_if_high_income","HIHIW"),
            ("urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_low_income","LILIW"),
            ("urbansim.household_x_gridcell.percent_mid_income_households_within_walking_distance_if_mid_income", "MIMIW"),
            ("urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_minority","MPMW"),
            ("urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_not_minority","NMPMW"),
            ("urbansim.household_x_gridcell.residential_units_when_household_has_children","UCH"),
#            ("urbansim.household_x_gridcell.young_household_in_high_density_residential","YHHD"),
#            ("gridcell.disaggregate(psrc.zone.ln_travel_time_weighted_access_to_employment_hbw_am_drive_alone)","GWAEDA"),            
#            ("generalized_cost_weighted_access_to_employment_hbw_am_transit_walk = ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))", 'GWAETW'),
            #("ln(gridcell.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk))", 'GWAETW'),
#            "urbansim.household_x_gridcell.same_household_age_in_faz",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk",
#             "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone",
#             "psrc.household_x_gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk_if_has_less_cars_than_workers",
#             "squared(psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk)",
#             "squared(psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone)"

#           ('gridcell.disaggregate(psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)', 'GC_CBD'),
             ]             
             
    }
