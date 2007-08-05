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

from variable_functions import my_attribute_label
from psrc.zone.employment_within_DDD_minutes_travel_time_hbw_am_transit_walk import employment_within_DDD_minutes_travel_time_hbw_am_transit_walk as psrc_employment_within_DDD_minutes_travel_time_hbw_am_transit_walk

class employment_within_DDD_minutes_travel_time_hbw_am_transit_walk(psrc_employment_within_DDD_minutes_travel_time_hbw_am_transit_walk):
    """total number of jobs for zones within DDD minutes travel time,
    The travel time used is for the home-based-work am trips by auto with
    drive-alone.
    """

    def dependencies(self):
        return ["psrc.travel_data.am_total_transit_time_walk",
                my_attribute_label("number_of_jobs")]
