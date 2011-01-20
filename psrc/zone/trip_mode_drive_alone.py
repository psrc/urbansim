# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.zone.abstract_trip_mode import AbstractTripMode

class trip_mode_drive_alone(AbstractTripMode):
    """ Trips for people driving alone"""
    def __init__(self):
        AbstractTripMode.__init__(self, matrices = [
                                      'hbw_daily_drive_alone_person_trip_table',
                                      'college_daily_drive_alone_person_trip_table',
                                      'hbnw_daily_drive_alone_person_trip_table',
                                      'nhb_daily_drive_alone_person_trip_table'
                                  ])
   

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.trip_mode_drive_alone"
                              
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
                 "hbw_daily_drive_alone_person_trip_table": array([1.1, 2.2, 3.3, 4.4]),
                 "college_daily_drive_alone_person_trip_table": array([1.0, 2.0, 3.0, 4.0]),
                 "hbnw_daily_drive_alone_person_trip_table": array([2.0, 3.0, 1.0, 0.0]),
                 "nhb_daily_drive_alone_person_trip_table": array([12.8, 4.5, 1.2, 8.0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([28.6, 24.9])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-4), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
                                     