# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from numpy import zeros, float32

class travel_time_hbw_am_drive_alone_to_DDD(Variable):
    """Travel time to the zone whose ID is the DDD.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    def __init__(self, number):
        self.tnumber = number
        self.variable_name = "travel_time_hbw_am_drive_alone_to_" + str(int(number))
        Variable.__init__(self)

    def dependencies(self):
        return ['travel_data.am_single_vehicle_to_work_travel_time']
    
    def compute(self, dataset_pool):
        zone_id = self.get_dataset().get_id_attribute()
        keys = map(lambda x: (x, self.tnumber), zone_id)
        travel_data = dataset_pool.get_dataset('travel_data')
        try:
            time = travel_data.get_attribute_by_id("am_single_vehicle_to_work_travel_time", keys)
        except:
            logger.log_warning("Variable %s returns zeros, since zone number %d is not in zoneset." % (self.variable_name, self.tnumber))
            time = zeros(self.get_dataset().size(), dtype=float32)
        return time


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