# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_travel_time_variable_for_non_interaction_dataset import abstract_travel_time_variable_for_non_interaction_dataset

class travel_time_hbw_am_drive_alone_to_DDD(abstract_travel_time_variable_for_non_interaction_dataset):
    """Travel time to the zone whose ID is the DDD.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    ##TODO: merge this variable with the same one in psrc/zone.
    _return_type = "float32"
    default_value = 999
    origin_zone_id = 'zone.zone_id'
    travel_data_attribute = 'travel_data.am_single_vehicle_to_work_travel_time'
           
    def __init__(self, number):
        self.destination_zone_id = 'destination_id=%s+0*zone.zone_id' % number
        abstract_travel_time_variable_for_non_interaction_dataset.__init__(self)

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    
    def get_values(self, number):
        self.variable_name = "eugene.zone.travel_time_hbw_am_drive_alone_to_%s" % number
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id":array([1,3])
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id":array([3,3,1,1]),
                "to_zone_id":array([1,3,1,3]),
                "am_single_vehicle_to_work_travel_time":array([1.1, 2.2, 3.3, 4.4])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        return values

    def test_to_1(self):
        values = self.get_values(1)
        should_be = array([3.3, 1.1])
        self.assert_(ma.allclose( values, should_be, rtol=1e-7), 
                     msg = "Error in " + self.variable_name)

    def test_to_3(self):
        values = self.get_values(3)
        should_be = array([4.4, 2.2])
        self.assert_(ma.allclose( values, should_be, rtol=1e-7), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()