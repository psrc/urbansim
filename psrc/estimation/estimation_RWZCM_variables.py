
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

specification = {
    -2:  #sub_model
        [
#         "household.household_id",
#         "zone.zone_id",
#         "psrc.household.worker1_work_place_zone_id",
#         "urbansim.household.zone_id as home_zone_id",
#         "psrc.household.home_zone_id as phome_zone_id",         
#         "ln(urbansim.zone.population)",
         "ln(urbansim.zone.number_of_jobs)",
#         "psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone",
         #"psrc.household_zone.worker1_travel_time_hbw_am_drive_alone_from_home_to_work",
         #"psrc.household_zone.worker1_am_total_transit_time_walk_from_home_to_work", 
         "psrc.person_x_zone.am_total_transit_time_walk_from_home_to_work",
         "psrc.person_x_zone.travel_time_hbw_am_drive_alone_from_home_to_work"
       ],

}