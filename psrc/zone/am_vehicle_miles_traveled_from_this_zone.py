# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_aggregate_travel_data_variable import abstract_aggregate_travel_data_variable

class am_vehicle_miles_traveled_from_this_zone(abstract_aggregate_travel_data_variable):
    """
    Calculate the vehicle miles traveled.
    """
    
    _return_type = "int32"
    fill_value = 0
    aggregate_function = 'sum'       #name of the numpy function to do the aggregate, e.g. sum, mean, 
    aggregate_zone_id = 'zone.zone_id'  
    aggregate_by_origin = True  #whether the aggregate_zone_id is origin zone
    travel_data_attribute = 'travel_data.am_vehicle_miles_traveled'

from numpy import ma, array
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.am_vehicle_miles_traveled_from_this_zone"
    
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
        
        should_be = array([5, 10])
        
        self.assertTrue(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
