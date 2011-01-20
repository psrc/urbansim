# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.zone.abstract_trip_weighted_average_variable_from_home import Abstract_Trip_Weighted_Average_Variable_From_Home

class trip_weighted_average_logsum_hbw_am_income_DDD(Abstract_Trip_Weighted_Average_Variable_From_Home):
    """ Trip weighted average generalized cost from home to any workplace for 
    home-based-work am trips by auto.
    """
    def __init__(self, income_break):        
        Abstract_Trip_Weighted_Average_Variable_From_Home.__init__(self, time_attribute_name = "logsum_hbw_am_income_" + str(income_break),
                                                         trips_attribute_name = "am_pk_period_drive_alone_vehicle_trips")

# TODO: unit test