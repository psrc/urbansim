# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_travel_time_variable_for_non_interaction_dataset import abstract_travel_time_variable_for_non_interaction_dataset

class am_vehicle_miles_traveled_to_DDD(abstract_travel_time_variable_for_non_interaction_dataset):
    """
    Calculate the vehicle miles traveled to the zone given by DDD.
    """
    
    _return_type = "float32"
    default_value = 999
    origin_zone_id = 'zone.zone_id'
    travel_data_attribute = 'travel_data.am_vehicle_miles_traveled'
           
    def __init__(self, number):
        self.destination_zone_id = 'destination_id=%s+0*zone.zone_id' % number
        abstract_travel_time_variable_for_non_interaction_dataset.__init__(self)
        
from numpy import ma, array
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.am_vehicle_miles_traveled_to_3"
    
    def test_my_input(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id': array([1, 3]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id":array([1,3,3,1]),
                "to_zone_id":  array([1,1,3,3]),
                "am_vehicle_miles_traveled":array([1, 7, 3, 4]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([4, 3 ])
        
        self.assertTrue(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()
