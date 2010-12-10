# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class SSS_from_home_to_work(abstract_travel_time_variable):
    """"""

    def __init__(self, mode):
        self.agent_zone_id = "person.disaggregate(urbansim_zone.household.zone_id)"
        self.location_zone_id = "zone.zone_id"
        self.travel_data_attribute = "urbansim.travel_data.%s" % mode
        self.direction_from_home = True
        abstract_travel_time_variable.__init__(self)
