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

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
    ## for the simtravel project
    'generalized_peak_travel_time_from_to_work = mag_zone.person_x_job.peak_travel_time_from_home_to_work + person.disaggregate(household.value_of_time) * mag_zone.person_x_job.peak_travel_distance_from_home_to_work_in_miles',
    'peak_travel_distance_from_home_to_work_in_miles = mag_zone.person_x_job.peak_travel_distance_from_home_to_work / 5280.0'
]
