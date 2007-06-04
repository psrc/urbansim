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
specification = {
 -2:  # submodel id
    [
    "constant",
    "psrc.gridcell.travel_time_hbw_am_drive_alone_to_cbd**2",
    #"squared(psrc.gridcell.travel_time_to_CBD)",
    "urbansim.gridcell.is_near_highway",
    "urbansim.gridcell.ln_residential_units",
    "urbansim.gridcell.ln_residential_units_within_walking_distance",
    "urbansim.gridcell.percent_low_income_households_within_walking_distance",
    "urbansim.gridcell.percent_open_space_within_walking_distance",
    "urbansim.gridcell.percent_water",
    #"urbansim.gridcell.travel_time_to_CBD",
    "psrc.gridcell.travel_time_hbw_am_drive_alone_to_cbd",
#    "urbansim.gridcell.is_near_highway",
#    "urbansim.gridcell.is_near_arterial",
#    "urbansim.gridcell.ln_residential_units",
#    "urbansim.gridcell.ln_residential_units_within_walking_distance",
##    "urbansim.gridcell.percent_residential_within_walking_distance",
#    "urbansim.gridcell.percent_open_space_within_walking_distance",
#    "urbansim.gridcell.percent_water",
#    "urbansim.gridcell.percent_low_income_households_within_walking_distance",
##    "urbansim.gridcell.ln_total_employment_within_walking_distance",
##    "urbansim.gridcell.percent_high_income_households_within_walking_distance",
##    "urbansim.gridcell.ln_service_sector_employment_within_walking_distance",
##    "urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",
##    "urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
##    "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk",
##    "psrc.gridcell.trip_weighted_average_time_hbw_from_home_am_drive_alone",
#    "squared(urbansim.gridcell.travel_time_to_CBD)",
#    "urbansim.gridcell.travel_time_to_CBD")
    ]
    }
