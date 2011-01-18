# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_weighted_access import abstract_weighted_access

class generalized_cost_weighted_access_to_population_hbw_am_drive_alone(abstract_weighted_access):
    """sum of number of jobs in zone j divided by generalized cost from zone i to j,
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    
    def __init__(self):
        self.aggregate_by_origin = True
        self.travel_data_attribute  = "travel_data.single_vehicle_to_work_travel_cost"
        self.zone_attribute_to_access = "zone.population"
        
        abstract_weighted_access.__init__(self)

from numpy import ma, array
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.generalized_cost_weighted_access_to_population_hbw_am_drive_alone"
    
    def test_my_input(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": array([1,3]),
                "population": array([10, 1]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id": array([3,3,1,1]),
                "to_zone_id": array([1,3,1,3]),
                "single_vehicle_to_work_travel_cost": array([1, 2, 3, 4]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([2.11111, 0.875])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)
        

if __name__=='__main__':
    opus_unittest.main()