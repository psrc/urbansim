# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.zone.abstract_mode_split import AbstractModeSplit

class mode_split_carpooling_over_automobile_trips(AbstractModeSplit):
    """ mode split for manual transportatoin to total trips"""
    def __init__(self):
        AbstractModeSplit.__init__(self, 
                                      path = 'psrc.zone',
                                      numerator_modes = [
                                          'trip_mode_share_ride2', 
                                          'trip_mode_share_ride3', 
                                      ],
                                      denominator_modes = [
                                          'trip_mode_drive_alone',
                                          'trip_mode_share_ride2', 
                                          'trip_mode_share_ride3',                                                      
                                      ]
                                  )
   

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.mode_split_carpooling_over_automobile_trips"
                              
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id":array([1,2]),
                "trip_mode_share_ride2": array([1,8]),
                "trip_mode_drive_alone": array([2,9]),
                "trip_mode_share_ride3": array([8,4]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([9.0/11.0, 12.0/21.0])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()                  