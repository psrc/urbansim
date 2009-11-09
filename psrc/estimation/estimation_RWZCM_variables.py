# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

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