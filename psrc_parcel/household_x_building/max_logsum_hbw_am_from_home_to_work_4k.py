# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.household_x_building.max_logsum_hbw_am_from_home_to_work import max_logsum_hbw_am_from_home_to_work

class max_logsum_hbw_am_from_home_to_work_4k(max_logsum_hbw_am_from_home_to_work):
    """max_logsum_hbw_am_from_home_to_work between worker1 & worker2 (for 4K model - uses different income breaks)"""
    
    def dependencies(self):
        return [ 
                "worker1_logsum_hbw_am_from_home_to_work = psrc_parcel.household_x_building.worker1_logsum_hbw_am_from_home_to_work_4k",
                "worker2_logsum_hbw_am_from_home_to_work = psrc_parcel.household_x_building.worker2_logsum_hbw_am_from_home_to_work_4k",
             ]
