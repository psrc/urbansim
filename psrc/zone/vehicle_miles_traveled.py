# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import array
from opus_core.ndimage import sum as ndimage_sum

class vehicle_miles_traveled(Variable):
    """
    Calculate the vehicle miles traveled.
    """
    
    _return_type = "float32"
   
    _am_VMT_attr = 'am_vehicle_miles_traveled'
    _md_VMT_attr = 'md_vehicle_miles_traveled'
    _pm_ev_ni_VMT_attr = 'pm_ev_ni_vehicle_miles_traveled'
        
    def dependencies(self):
        return [attribute_label("travel_data", self._am_VMT_attr), 
                attribute_label("travel_data", self._md_VMT_attr),
                attribute_label("travel_data", self._pm_ev_ni_VMT_attr)]

    def compute(self, dataset_pool):
        """
        zone_ids = zone_set.get_attribute('zone_id')
        am_VMT = travel_data.get_attribute(self._am_VMT_attr)
        md_VMT = travel_data.get_attribute(self._md_VMT_attr)
        pm_ev_ni_VMT = travel_data.get_attribute(self._pm_ev_ni_VMT_attr)
        """
        
        zone_ids = self.get_dataset().get_id_attribute()
        travel_data = dataset_pool.get_dataset('travel_data')
        
        from_zone_id = travel_data.get_attribute("from_zone_id")       
        
        am_VMT_attr = travel_data.get_attribute(self._am_VMT_attr)  
        md_VMT_attr = travel_data.get_attribute(self._md_VMT_attr)  
        pm_ev_ni_VMT_attr = travel_data.get_attribute(self._pm_ev_ni_VMT_attr)  
        
        results =   array(ndimage_sum(am_VMT_attr, labels = from_zone_id, index=zone_ids)) + \
                    array(ndimage_sum(md_VMT_attr, labels = from_zone_id, index=zone_ids)) + \
                    array(ndimage_sum(pm_ev_ni_VMT_attr, labels = from_zone_id, index=zone_ids))        
        
        return results
        

from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.vehicle_miles_traveled"
    
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
                "am_vehicle_miles_traveled":array([1, 7, 3, 4]),
                "md_vehicle_miles_traveled":array([1, 1, 2, 2]),
                "pm_ev_ni_vehicle_miles_traveled":array([0, 3, 0, 1]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([9, 16])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
  