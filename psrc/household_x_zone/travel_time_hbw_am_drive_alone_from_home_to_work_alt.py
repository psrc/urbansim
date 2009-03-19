# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from psrc.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class travel_time_hbw_am_drive_alone_from_home_to_work_alt(abstract_travel_time_variable):
    """travel_time_hbw_am_drive_alone_from_home_to_work"""

    agent_zone_id = "psrc.household.home_zone_id_from_grid_id"
    location_zone_id = "urbansim.zone.zone_id"
    travel_data_attribute = "urbansim.travel_data.am_single_vehicle_to_work_travel_time"

from numpy import ma, array
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from psrc.opus_package_info import package
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from psrc.datasets.person_x_zone_dataset import PersonXZoneDataset

from psrc.datasets.person_dataset import PersonDataset
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_zone.travel_time_hbw_am_drive_alone_from_home_to_work_alt"

    def test_my_inputs(self):

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {
             "household":{
                 "household_id":array([1,2,3,4,5]),
                 "home_zone_id_from_grid_id":array([3, 1, 1, 1, 2]),
                 },
             "zone":{
                     "zone_id":array([1,  2,  3]),
                     },
             "travel_data":{
                 "from_zone_id":              array([3,   3,   1,   1,   1,   2,   2,   3,   2]),
                 "to_zone_id":                array([1,   3,   1,   3,   2,   1,   3,   2,   2]),
                 "am_single_vehicle_to_work_travel_time":array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])}},
            dataset = "household_x_zone")
        default_value = travel_time_hbw_am_drive_alone_from_home_to_work_alt.default_value
        should_be = array([[1.1, 7.8, 2.2],
                           [3.3, 0.5, 4.4], [3.3, 0.5, 4.4],
                           [3.3, 0.5, 4.4], [0.7, 1.0, 8.7]])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()