
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

all_variables = [
#    "hh_income = person.disaggregate(household.income)",
#    "hh_size = person.disaggregate(household.persons)",
#    "person.age",
#    "person.work_at_home",
#    "person.edu",         
    "hh_income_x_job_is_in_employment_sector_group_fires = person.disaggregate(household.income) * urbansim.job.is_in_employment_sector_group_fires",    
    "psrc_parcel.person_x_job.income_and_am_total_transit_time_walk_from_home_to_work",
    "psrc_parcel.person_x_job.travel_time_hbw_am_drive_alone_from_home_to_work",
    "psrc_parcel.person_x_job.am_total_transit_time_walk_from_home_to_work",
    ]

specification = {}

specification = {
    "_definition_": all_variables,                               
    -2:
        [
         'hh_income_x_job_is_in_employment_sector_group_fires',
         #"psrc_parcel.person_x_job.income_and_am_total_transit_time_walk_from_home_to_work",
         "psrc_parcel.person_x_job.travel_time_hbw_am_drive_alone_from_home_to_work",
         #"psrc_parcel.person_x_job.am_total_transit_time_walk_from_home_to_work",

    ],                             
}
