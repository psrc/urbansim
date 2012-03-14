# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_access_within_threshold_variable import abstract_access_within_threshold_variable

class number_of_public_schools_within_DDD_minutes_am_walk(abstract_access_within_threshold_variable):

    def __init__(self, threshold):
        self.threshold = threshold
        self.travel_data_attribute  = "travel_data.am_walk_time_in_minutes"
        self.zone_attribute_to_access = "zone.aggregate(psrc_parcel.parcel.number_of_public_schools)"
        
        abstract_access_within_threshold_variable.__init__(self)
