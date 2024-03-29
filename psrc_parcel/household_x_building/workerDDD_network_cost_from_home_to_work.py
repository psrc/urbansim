# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class workerDDD_network_cost_from_home_to_work(abstract_travel_time_variable):
    """single vehicle travel cost from the centroid of home zone to that of work zone"""

    def __init__(self, number):
        self.default_value = 0
        self.agent_zone_id = "work%s_workplace_zone_id = household.aggregate((psrc.person.worker%s == 1) * urbansim_parcel.person.workplace_zone_id ).astype(int32)" % (number, number)
        self.location_zone_id = "urbansim_parcel.building.zone_id"
        self.travel_data_attribute = "urbansim.travel_data.single_vehicle_to_work_travel_cost"
        self.direction_from_home = False
        abstract_travel_time_variable.__init__(self)



if __name__=='__main__':
    opus_unittest.main()
