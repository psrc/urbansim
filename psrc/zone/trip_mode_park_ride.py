# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from psrc.zone.abstract_trip_mode import AbstractTripMode

class trip_mode_park_ride(AbstractTripMode):
    """ Trips for people driving alone"""
    def __init__(self):
        AbstractTripMode.__init__(self, matrices = [
                                      'hbw_daily_drive_to_park_ride_person_trip_table',
                                  ])
   

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.trip_mode_park_ride"
                              
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id': array([1, 2]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id": array([1,1,2,2]),
                "to_zone_id":array([1,2,1,2]),
                'hbw_daily_drive_to_park_ride_person_trip_table': array([1.1, 2.2, 3.3, 4.4]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([3.3, 7.7])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
              