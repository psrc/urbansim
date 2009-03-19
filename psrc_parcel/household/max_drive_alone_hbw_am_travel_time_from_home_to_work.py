# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from psrc.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable
from opus_core.variables.variable import Variable
from numpy import newaxis, concatenate

class max_drive_alone_hbw_am_travel_time_from_home_to_work(Variable):
    """max_drive_alone_hbw_am_travel_time_from_home_to_work between worker1 & worker2"""
    
    def dependencies(self):
        return [ 
                "psrc_parcel.household.worker1_drive_alone_from_home_to_work",
                "psrc_parcel.household.worker2_drive_alone_from_home_to_work",
             ]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        data1 = dataset.get_attribute("worker1_drive_alone_from_home_to_work")
        data2 = dataset.get_attribute("worker2_drive_alone_from_home_to_work")

        return concatenate((data1[...,newaxis], data2[...,newaxis]), axis=1).max(axis=1)
    
from numpy import ma, array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger
from workerDDD_drive_alone_from_home_to_work import workerDDD_drive_alone_from_home_to_work

class Tests(opus_unittest.OpusTestCase):

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
                'worker2':           array([0, 0, 0, 0, 1, 0, 0, 0]),
                'workplace_zone_id': array([1, 3, 3, 2, 2, 3, -1, -1]),
                },
             'household': {
                'household_id':array([1, 2, 3, 4, 5]),
                'zone_id':     array([3, 1, 1, 1, 2]),
                },
            'travel_data': {
                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                'to_zone_id':  array([1,3,1,3,2,1,3,2,2]),
                'am_single_vehicle_to_work_travel_time':array([1.1, 2.2, 3.3, 4.4, 6.5, 0.7, 8.7, 7.8, 1.0])
            }
        })
        default_value = workerDDD_drive_alone_from_home_to_work.default_value
        should_be = array([1.1, 4.4, 6.5, default_value, default_value])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()