# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable_for_non_interaction_dataset import abstract_travel_time_variable_for_non_interaction_dataset

class peak_travel_time_from_home_to_work(abstract_travel_time_variable_for_non_interaction_dataset):
    """"""

    default_value = -1
    origin_zone_id = "person.disaggregate(building.zone_id,intermediates=[household])"
    destination_zone_id = "mag_zone.person.wtaz"
    travel_data_attribute = "travel_data.peak_travel_time"
