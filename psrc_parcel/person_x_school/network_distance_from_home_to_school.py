# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class network_distance_from_home_to_school(abstract_travel_time_variable):
    """single vehicle travel distance from the centroid of home zone to that of school zone"""

    agent_zone_id = "urbansim_parcel.person.zone_id"
    location_zone_id = "psrc_parcel.school.zone_id"
    travel_data_attribute = "urbansim.travel_data.single_vehicle_to_work_travel_distance"
