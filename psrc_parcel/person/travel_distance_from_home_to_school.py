# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable_for_non_interaction_dataset import abstract_travel_time_variable_for_non_interaction_dataset

class travel_distance_from_home_to_school(abstract_travel_time_variable_for_non_interaction_dataset):
    """travel distance from home to school"""

    default_value = 0
    origin_zone_id = "residence_zone_id = person.disaggregate(urbansim_parcel.household.zone_id)"
    destination_zone_id = "psrc_parcel.person.attending_school_zone_id"
    travel_data_attribute = "urbansim.travel_data.single_vehicle_to_work_travel_distance"
