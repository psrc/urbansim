# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.zone.abstract_mode_split import AbstractModeSplit

class mode_split_bike_trips_over_all(AbstractModeSplit):
    """ mode split for manual transportatoin to total trips"""
    def __init__(self):
        AbstractModeSplit.__init__(self, 
                                      path = 'psrc.zone',
                                      numerator_modes = [
                                          'trip_mode_bike'
                                      ],
                                      denominator_modes = [
                                          'trip_mode_bike',
                                          'trip_mode_walk', 
                                          'trip_mode_park_ride',
                                          'trip_mode_drive_alone',
                                          'trip_mode_share_ride2', 
                                          'trip_mode_share_ride3', 
                                          'trip_mode_transit',                                                          
                                      ]
                                  )
   

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.mode_split_bike_trips_over_all"
                              
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": array([1,2]),
                "trip_mode_bike": array([3,1]),
                "trip_mode_walk": array([5,6]),
                "trip_mode_park_ride": array([3,2]),
                "trip_mode_share_ride2": array([1,8]),
                "trip_mode_drive_alone": array([2,9]),
                "trip_mode_share_ride3": array([8,4]),
                "trip_mode_transit": array([5,5]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id": array([1,1,2,2]),
                "to_zone_id":array([1,2,1,2]),
                "hbw_daily_share_ride3_person_trip_table": array([1.1, 2.2, 3.3, 4.4]),
                "hbnw_daily_share_ride3_person_trip_table": array([2.0, 3.0, 1.0, 0.0]),
                "nhb_daily_share_ride3_person_trip_table": array([12.8, 4.5, 1.2, 8.0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([3.0/27.0, 1.0/35.0])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-4), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()                   