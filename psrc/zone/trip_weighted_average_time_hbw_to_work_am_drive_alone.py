# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from psrc.zone.abstract_trip_weighted_average_variable_to_work import Abstract_Trip_Weighted_Average_Variable_To_Work

class trip_weighted_average_time_hbw_to_work_am_drive_alone(Abstract_Trip_Weighted_Average_Variable_To_Work):
    """ Trip weighted average time from home to any work for 
    home-based-work am trips by auto.
    """
    def __init__(self):
        Abstract_Trip_Weighted_Average_Variable_To_Work.__init__(self, time_attribute_name = "am_single_vehicle_to_work_travel_time",
                                                         trips_attribute_name = "am_pk_period_drive_alone_vehicle_trips")
    

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.trip_weighted_average_time_hbw_to_work_am_drive_alone"
    
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
                "from_zone_id":array([1,1,2,2]),
                "to_zone_id":array([1,2,1,2]),
                "am_single_vehicle_to_work_travel_time":array([1.1, 2.2, 3.3, 4.4]),
                "am_pk_period_drive_alone_vehicle_trips":array([1.0, 2.0, 3.0, 4.0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([(1.1*1.0 +3.3*3.0)/(4.0), 
                           (2.2*2.0 + 4.4*4.0)/(6.0)])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)

    def test_with_zero_denominator(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": array([1,2,3,4]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id":array([1,2,1,2,2]),
                "to_zone_id":array([1,2,2,3,4]),
                "am_single_vehicle_to_work_travel_time":array([1.1, 2.2, 3.3, 4.4, 5.5]),
                "am_pk_period_drive_alone_vehicle_trips":array([0.0, 20.0, 30.0, 0.0, 0.0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([(2.2*20.0 + 3.3*30)/(20.0+30.0), 
                           (2.2*20.0 + 3.3*30)/(20.0+30.0), 
                           (2.2*20.0 + 3.3*30)/(20.0+30.0),# when denominator = 0, use prior good value
                           (2.2*20.0 + 3.3*30)/(20.0+30.0)])# when denominator = 0, use prior good value
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)

    def test_with_all_zero_denominator(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": array([1,2,3,4]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id":array([1,2,1,2,2]),
                "to_zone_id":array([1,2,2,3,4]),
                "am_single_vehicle_to_work_travel_time":array([1.1, 2.2, 3.3, 4.4, 5.5]),
                "am_pk_period_drive_alone_vehicle_trips":array([0.0, 0.0, 0.0, 0.0, 0.0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([0.0, 
                           0.0, 
                           0.0,
                           0.0 ])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()