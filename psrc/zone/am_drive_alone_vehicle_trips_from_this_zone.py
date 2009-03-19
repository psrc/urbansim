# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import array
from scipy.ndimage import sum as ndimage_sum

class am_drive_alone_vehicle_trips_from_this_zone(Variable):
    """
    Calculate the sum of drive alone trips originating from  each zone.
    """
    
    _return_type = "int32"
   
    _am_attr = 'am_pk_period_drive_alone_vehicle_trips'
        
    def dependencies(self):
        return [attribute_label("travel_data", self._am_attr)]

    def compute(self, dataset_pool):
        
        zone_ids = self.get_dataset().get_id_attribute()
        travel_data = dataset_pool.get_dataset('travel_data')
        
        from_zone_id = travel_data.get_attribute("from_zone_id")       
        
        am_attr = travel_data.get_attribute(self._am_attr)  
        
        results =   array(ndimage_sum(am_attr, labels = from_zone_id, index=zone_ids))        
        
        return results
        

from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.am_drive_alone_vehicle_trips_from_this_zone"
    
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
                "to_zone_id":array([1,1,1,1]),
                "am_pk_period_drive_alone_vehicle_trips":array([1, 7, 3, 4]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([5, 10])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
  