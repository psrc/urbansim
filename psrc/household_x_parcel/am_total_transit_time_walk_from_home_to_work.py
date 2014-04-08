# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class am_total_transit_time_walk_from_home_to_work(abstract_travel_time_variable):
    """travel_time_hbw_am_drive_alone_from_home_to_work"""

    agent_zone_id = "urbansim.household.work_place_zone_id"
    location_zone_id = "urbansim.parcel.zone_id"
    travel_data_attribute = "urbansim.travel_data.am_total_transit_time_walk"
    direction_from_home = False
