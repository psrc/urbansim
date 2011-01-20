# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_weighted_access import abstract_weighted_access

class travel_time_weighted_access_to_employment_hbw_am_walk(abstract_weighted_access):
    """sum of number of jobs in zone j divided by travel time from zone i to j,
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    
    def __init__(self):
        self.aggregate_by_origin = False
        self.travel_data_attribute  = "travel_data.am_walk_time_in_minutes"
        self.zone_attribute_to_access = "zone.number_of_jobs"
        
        abstract_weighted_access.__init__(self)
    
#    def dependencies(self):
#        return ["psrc.travel_data.am_walk_time_in_minutes",
#                "urbansim.zone.number_of_jobs"]
#    
#    def compute(self, dataset_pool):
#        zone_ids = self.get_dataset().get_id_attribute()
#        travel_data = dataset_pool.get_dataset('travel_data')
#        time = power(travel_data.get_attribute('am_walk_time_in_minutes'), 2)
#        
#        to_zone_id = travel_data.get_attribute("to_zone_id")
#        zone_index = self.get_dataset().get_id_index(to_zone_id)
#        num_jobs = self.get_dataset().get_attribute('number_of_jobs')[zone_index]
#
#        from_zone_id = travel_data.get_attribute("from_zone_id")        
#        results = array(ndimage_sum(num_jobs / time.astype(float32), labels = from_zone_id, index=zone_ids))
#        
#        return results


from numpy import ma, array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.travel_time_weighted_access_to_employment_hbw_am_walk"
    
    def test_my_input(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": array([1,3]),
                "number_of_jobs": array([10, 1]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id":array([3,3,1,1]),
                "to_zone_id":array([1,3,1,3]),
                "am_walk_time_in_minutes":array([1, 2, 3, 4]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([1.17361, 10.25])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)
        

if __name__=='__main__':
    opus_unittest.main()