# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from psrc.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class workerDDD_transit_walk_hbw_am_travel_time_from_home_to_work(abstract_travel_time_variable):
    """transit_walk_hbw_am_travel_time_from_home_to_work"""

    def __init__(self, number):
        self.default_value = 0
        self.agent_zone_id = "work%s_workplace_zone_id = household.aggregate((person.worker%s == 1).astype(int32) * urbansim_parcel.person.workplace_zone_id)" % (number, number)
        self.location_zone_id = "urbansim_parcel.building.zone_id"
        self.travel_data_attribute = "urbansim.travel_data.am_total_transit_time_walk"
        self.direction_from_home = False
        abstract_travel_time_variable.__init__(self)

#from numpy import ma, array
#from opus_core.tests import opus_unittest
#from opus_core.datasets.dataset_pool import DatasetPool
#from opus_core.storage_factory import StorageFactory
#from opus_core.logger import logger
#
#class Tests(opus_unittest.OpusTestCase):
#    variable_name = 'psrc.household_x_parcel.worker1_am_total_transit_time_walk_from_home_to_work'
#
#    def setUp(self):
#        logger.enable_hidden_error_and_warning_words()
#
#    def tearDown(self):
#        logger.disable_hidden_error_and_warning_words()
#
#    def test_my_inputs(self):
#        storage = StorageFactory().get_storage('dict_storage')
#
#        storage.write_table(
#            table_name='persons',
#            table_data={
#                'person_id':array([1, 2, 3, 4, 5, 6]),
#                'household_id':array([1, 1, 2, 3, 3, 3]),
#                'member_id':array([1, 2, 1, 1, 2, 3]),
#                'worker1':array([1, 0, 1, 0, 0, 1]),
#                'work_place_zone_id':array([1, 3, 3, 2, 1, 3])
#                },
#        )
#        storage.write_table(
#            table_name='parcels',
#            table_data={
#                'parcel_id':array([1,2,3,4]),
#                'zone_id':array([1, 1, 3, 2])
#                },
#        )
#        storage.write_table(
#            table_name='households',
#            table_data={
#                'household_id':array([1,2,3,4,5]),
#                'zone_id':array([3, 1, 1, 1, 2]),
#                },
#        )
#        storage.write_table(
#            table_name='travel_data',
#            table_data={
#                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
#                'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
#                'am_total_transit_time_walk':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
#            }
#        )
#
#        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
#                                   storage=storage)
#
#        household_x_parcel = dataset_pool.get_dataset('household_x_parcel')
#        household_x_parcel.compute_variables(self.variable_name,
#                                             dataset_pool=dataset_pool)
#        values = household_x_parcel.get_attribute(self.variable_name)
#
#        default_value = workerDDD_am_total_transit_time_walk_from_home_to_work.default_value
#        should_be = array([[3.3, 3.3, 1.1, 0.7],
#                           [4.4, 4.4, 2.2, 8.7],
#                           [4.4, 4.4, 2.2, 8.7],
#                           [default_value, default_value, default_value, default_value],
#                           [default_value, default_value, default_value, default_value]])
#
#        self.assert_(ma.allclose(values, should_be, rtol=1e-3),
#                     msg="Error in " + self.variable_name)
#
#
#if __name__=='__main__':
#    opus_unittest.main()