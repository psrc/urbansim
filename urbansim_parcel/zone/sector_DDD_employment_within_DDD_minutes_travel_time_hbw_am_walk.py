# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_access_within_threshold_variable import abstract_access_within_threshold_variable

class sector_DDD_employment_within_DDD_minutes_travel_time_hbw_am_walk(abstract_access_within_threshold_variable):
    """total number of jobs for zones within DDD minutes travel time,
    """
    def __init__(self, sector, threshold):
        self.threshold = threshold
        self.travel_data_attribute  = "travel_data.am_walk_time_in_minutes"
        self.zone_attribute_to_access = "urbansim_parcel.zone.number_of_jobs_of_sector_" + str(sector)
        
        abstract_access_within_threshold_variable.__init__(self)

