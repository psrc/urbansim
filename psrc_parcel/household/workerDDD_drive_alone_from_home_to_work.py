# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.abstract_variables.abstract_travel_time_variable_1d import abstract_travel_time_variable_1d

class workerDDD_drive_alone_from_home_to_work(abstract_travel_time_variable_1d):
    """drive_alone_from_home_to_work"""

    default_value = 0
    
    def __init__(self, number):
        self.agent_zone_id = "urbansim_parcel.household.zone_id"
        self.location_zone_id = "work%s_workplace_zone_id = household.aggregate((person.worker%s == 1).astype(int32) * urbansim_parcel.person.workplace_zone_id)" % (number, number)
        self.travel_data_attribute = "urbansim.travel_data.am_single_vehicle_to_work_travel_time"
        self.direction_from_home = True
        abstract_travel_time_variable_1d.__init__(self)

from numpy import ma, array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.household.worker1_drive_alone_from_home_to_work"

    def setUp(self):
        logger.enable_hidden_error_and_warning_words()

    def tearDown(self):
        logger.disable_hidden_error_and_warning_words()

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            'person': {
                'person_id':array([1, 2, 3, 4, 5, 6, 7, 8]),
                'household_id':      array([1, 1, 2, 3, 3, 3, 4, 5]),
                'worker1':           array([1, 0, 1, 0, 0, 1, 0, 0]),
                'workplace_zone_id':array([1, 3, 3, 2, 1, 3, -1, -1]),
                },
             'household': {
                'household_id':array([1,2,3,4,5]),
                'zone_id':array([3, 1, 1, 1, 2]),
                },
            'travel_data': {
                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                'to_zone_id':  array([1,3,1,3,2,1,3,2,2]),
                'am_single_vehicle_to_work_travel_time':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
            }
        })
        default_value = workerDDD_drive_alone_from_home_to_work.default_value
        should_be = array([1.1, 4.4, 4.4, default_value, default_value])
        tester.test_is_close_for_family_variable(self, should_be, self.variable_name)


if __name__=='__main__':
    opus_unittest.main()