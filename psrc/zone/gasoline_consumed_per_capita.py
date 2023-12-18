# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable

class gasoline_consumed_per_capita(Variable):
    """
    Calculate the gasoline consumed per capita.
    """
    
    _return_type = "float32"
        
    def dependencies(self):
        return ['psrc.zone.vehicle_miles_traveled_per_capita']

    def compute(self, dataset_pool):
        """average miles per gallon of gasoline"""
        miles_per_gallon = 21.5
        zone_set = self.get_dataset()
        vehicle_miles_traveled_per_capita = zone_set.get_attribute('vehicle_miles_traveled_per_capita')
        return vehicle_miles_traveled_per_capita / miles_per_gallon
    

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.gasoline_consumed_per_capita"
    
    def test_my_input(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id":array([1,2,3]),
                "population":array([2,0,4]),
                "vehicle_miles_traveled_per_capita":array([47.0,114.0,12.0])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([2.186, 5.302, 0.558])
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
  