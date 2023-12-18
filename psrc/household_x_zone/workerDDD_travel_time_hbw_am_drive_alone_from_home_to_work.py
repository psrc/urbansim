# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class workerDDD_travel_time_hbw_am_drive_alone_from_home_to_work(abstract_travel_time_variable):
    """travel_time_hbw_am_drive_alone_from_home_to_work"""

    def __init__(self, number):
        self.agent_zone_id = "psrc.household.worker%s_work_place_zone_id" % number
        self.location_zone_id = "urbansim.zone.zone_id"
        self.travel_data_attribute = "urbansim.travel_data.am_single_vehicle_to_work_travel_time"
        self.direction_from_home = False
        abstract_travel_time_variable.__init__(self)

from numpy import ma, array
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_zone.worker1_travel_time_hbw_am_drive_alone_from_home_to_work"

    def setUp(self):
        logger.enable_hidden_error_and_warning_words()

    def tearDown(self):
        logger.disable_hidden_error_and_warning_words()

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        persons_table_name = 'persons'

        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5, 6]),
                    'household_id':array([1, 1, 2, 3, 3, 3]),
                    'member_id':array([1, 2, 1, 1, 2, 3]),
                    'worker1':array([1, 0, 1, 0, 0, 1]),
                    'work_place_zone_id':array([1, 3, 3, 2, 1, 3])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'household':{
                    'household_id':array([1,2,3,4,5]),
                    'zone_id':array([3, 1, 1, 1, 2]),
                    },
                'zone':{
                    'zone_id':array([1, 3, 2]),
                    },
                'person':persons,
                'travel_data':{
                    'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                    'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
                    'am_single_vehicle_to_work_travel_time':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0]),
                    }
                },
            dataset = 'household_x_zone'
            )

        default_value = workerDDD_travel_time_hbw_am_drive_alone_from_home_to_work.default_value
        should_be = array([[3.3, 1.1, 0.7], [4.4,2.2, 8.7],
                           [4.4, 2.2, 8.7], [default_value, default_value, default_value],
                           [default_value, default_value, default_value]])

        self.assertTrue(ma.allclose(values, should_be, rtol=1e-3),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()