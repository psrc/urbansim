# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class am_total_transit_time_walk_from_home_to_school(abstract_travel_time_variable):
    """am_total_transit_time_walk_from_home_to_school"""

    agent_zone_id = "urbansim_parcel.person.zone_id"
    location_zone_id = "psrc_parcel.school.zone_id"
    travel_data_attribute = "urbansim.travel_data.am_total_transit_time_walk"
