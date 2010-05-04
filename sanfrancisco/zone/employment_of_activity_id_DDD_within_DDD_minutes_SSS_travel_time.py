# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_access_within_threshold_variable import abstract_access_within_threshold_variable

class employment_of_activity_id_DDD_within_DDD_minutes_SSS_travel_time(abstract_access_within_threshold_variable):
    """total number of jobs for zones within DDD minutes SSS (mode) travel time,
    """
    
    _return_type = "int32"
    function = "sum"

    def __init__(self, activitynum, number, mode):
        self.activity_id=activitynum
        self.threshold = number
        self.travel_data_attribute  = "travel_data.%s" % mode
        #*(business.activity_id==self.activity_id)
        self.zone_attribute_to_access = "emp_access=zone.aggregate(business.employment*(business.activity_id==%d),intermediates=[building,parcel])" % self.activity_id
        abstract_access_within_threshold_variable.__init__(self)
