# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class from_origin_to_destination_travel_data_SSS(abstract_travel_time_variable):
    """"""

    def __init__(self, attribute_name):
        self.default_value = 0
        self.agent_zone_id = "person_trip.from_zone_id"
        self.location_zone_id = "zone.zone_id"
        self.travel_data_attribute = "travel_data." + attribute_name
        self.direction_from_home = True
        abstract_travel_time_variable.__init__(self)
