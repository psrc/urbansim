# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class single_vehicle_to_destination_travel_cost(abstract_travel_time_variable):
    """drive_alone_hbw_am_travel_time_from_home_to_work"""

    def __init__(self):
        self.default_value = 0
        self.agent_zone_id = "person_trip.from_zone_id"
        self.location_zone_id = "zone.zone_id"
        self.travel_data_attribute = "urbansim.travel_data.single_vehicle_to_work_travel_cost"
        self.direction_from_home = True
        abstract_travel_time_variable.__init__(self)
