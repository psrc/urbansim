# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable

class greenhouse_gas_emissions_from_vehicle_travel(Variable):
    """
    Calculate the total greenhouse gas emissions for a year.
    """
    _return_type = "float32"
        
    def dependencies(self):
        return ["psrc.zone.vehicle_miles_traveled"]
    
    def compute(self, dataset_pool):
        """carbon dioxide coefficient from INDEX variable"""
        co2_pounds_per_vehicle_mile = .916
        vmt = self.get_dataset().get_attribute("vehicle_miles_traveled")
        return co2_pounds_per_vehicle_mile * vmt
        

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.greenhouse_gas_emissions_from_vehicle_travel"
    
    def test_my_input(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id":array([1,3]),
                "vehicle_miles_traveled":array([2,4])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([1.832, 3.664])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
  