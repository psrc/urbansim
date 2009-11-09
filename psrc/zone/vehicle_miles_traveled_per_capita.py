# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import where

class vehicle_miles_traveled_per_capita(Variable):
    """
    Calculate the vehicle miles traveled per capita.
    """
    
    _return_type = "float32"
        
    def dependencies(self):
        return ['psrc.zone.vehicle_miles_traveled',
                attribute_label("zone","population")]

    def compute(self, dataset_pool):
        zone_set = self.get_dataset()
        
        population = zone_set.get_attribute("population")
        population[where(population==0)] = 1
        
        vehicle_miles_traveled = zone_set.get_attribute('vehicle_miles_traveled')
        
        return vehicle_miles_traveled / population 
        

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.vehicle_miles_traveled_per_capita"
    
    def test_my_input(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id":array([1,2,3]),
                "population":array([2,0,4]),
                "vehicle_miles_traveled":array([9.0,4.0,16.0]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id":array([1,3,3,1,2]),
                "to_zone_id":array([1,1,1,1,2]),
                "am_vehicle_miles_traveled": array([1, 7, 3, 4, 3]),
                "md_vehicle_miles_traveled": array([1, 1, 2, 2, 1]),
                "pm_ev_ni_vehicle_miles_traveled": array([0, 3, 0, 1, 0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([4.5, 4, 4])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
  