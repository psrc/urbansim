# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from mag_zone.abstract_variables.abstract_access_within_threshold_variable import abstract_access_within_threshold_variable

class SSS_within_DDD_SSS_threshold(abstract_access_within_threshold_variable):
    """sum zone attribute SSS (e.g. number of jobs) within DDD minutes SSS (primary attribute of travel_data, e.g. travel time by mode),
    e.g. urbansim_zone.zone.number_of_jobs_within_30_hbw_am_drive_alone_threshold
    """
    
    _return_type = "int32"
    function = "sum"

    def __init__(self, zone_attribute, number, mode):
        self.zone_attribute_to_access =  "mag_zone.tazi03.%s" % zone_attribute
        self.threshold = number
        self.travel_data_attribute  = "travel_data.%s" % mode
        abstract_access_within_threshold_variable.__init__(self)