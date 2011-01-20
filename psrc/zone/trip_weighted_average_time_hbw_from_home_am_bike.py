# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.zone.abstract_trip_weighted_average_variable_from_home import Abstract_Trip_Weighted_Average_Variable_From_Home

class trip_weighted_average_time_hbw_from_home_am_bike(Abstract_Trip_Weighted_Average_Variable_From_Home):
    """ Trip weighted average time from home to any workplace for 
    home-based-work am trips by auto.
    """
    def __init__(self):
        Abstract_Trip_Weighted_Average_Variable_From_Home.__init__(self, time_attribute_name = "am_bike_to_work_travel_time",
                                                         trips_attribute_name = "am_biking_person_trips")
