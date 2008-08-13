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

from psrc.zone.abstract_trip_weighted_average_variable_to_work import Abstract_Trip_Weighted_Average_Variable_To_Work

class trip_weighted_average_time_hbw_to_work_am_bike(Abstract_Trip_Weighted_Average_Variable_To_Work):
    """ Trip weighted average time from home to any workplace for 
    home-based-work am trips by auto.
    """
    def __init__(self):
        Abstract_Trip_Weighted_Average_Variable_To_Work.__init__(self, time_attribute_name = "am_bike_to_work_travel_time",
                                                         trips_attribute_name = "am_biking_person_trips")
