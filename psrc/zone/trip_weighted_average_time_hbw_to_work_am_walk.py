# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from psrc.zone.abstract_trip_weighted_average_variable_to_work import Abstract_Trip_Weighted_Average_Variable_To_Work

class trip_weighted_average_time_hbw_to_work_am_walk(Abstract_Trip_Weighted_Average_Variable_To_Work):
    """ Trip weighted average time from home to any workplace for 
    home-based-work am trips by auto.
    """
    def __init__(self):
        Abstract_Trip_Weighted_Average_Variable_To_Work.__init__(self, time_attribute_name = "am_walk_time_in_minutes",
                                                         trips_attribute_name = "am_walking_person_trips")
