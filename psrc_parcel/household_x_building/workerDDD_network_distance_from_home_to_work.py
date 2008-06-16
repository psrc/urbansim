#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#
from psrc.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class workerDDD_network_distance_from_home_to_work(abstract_travel_time_variable):
    """single vehicle travel distance from the centroid of home zone to that of work zone"""

    def __init__(self, number):
        self.default_value = 0
        self.agent_zone_id = "work%s_workplace_zone_id = household.aggregate((person.worker%s == 1).astype(int32) * urbansim_parcel.person.workplace_zone_id )" % (number, number)
        self.location_zone_id = "urbansim_parcel.building.zone_id"
        self.travel_data_attribute = "urbansim.travel_data.single_vehicle_to_work_travel_distance"
        self.direction_from_home = False
        abstract_travel_time_variable.__init__(self)



if __name__=='__main__':
    opus_unittest.main()
