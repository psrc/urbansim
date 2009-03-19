# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import array, zeros
from opus_core.logger import logger


class am_vehicle_miles_traveled_to_DDD(Variable):
    """
    Calculate the vehicle miles traveled to the zone given by DDD.
    """
    
    _return_type = "float32"
   
    _am_VMT_attr = 'am_vehicle_miles_traveled'
        
    def __init__(self, number):
        self.tnumber = number
        self.variable_name = "am_vehicle_miles_traveled_to_" + str(int(number))
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("travel_data", self._am_VMT_attr)]

    def compute(self, dataset_pool):
        
        zone_ids = self.get_dataset().get_id_attribute()
        travel_data = dataset_pool.get_dataset('travel_data')
        keys = map(lambda x: (x, self.tnumber), zone_ids)
        try:
            miles = travel_data.get_attribute_by_id(self._am_VMT_attr, keys)
        except:
            logger.log_warning("Variable %s returns zeros, since zone number %d is not in zoneset." % (self.variable_name, self.tnumber))
            miles = zeros(self.get_dataset().size(), dtype=self._return_type)
        return miles
        

from numpy import ma

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
        
        self.assert_(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
  