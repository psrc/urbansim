# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class peak_travel_time_from_home_to_work(abstract_travel_time_variable):
    """peak_travel_time_from_home_to_work"""

    agent_zone_id = "household.aggregate(mag_zone.person.wtaz, function=maximum)"
    location_zone_id = "building.zone_id"
    travel_data_attribute = "urbansim.travel_data.peak_travel_time"

