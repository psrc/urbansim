# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable

class income_and_am_total_transit_time_walk_from_home_to_work(Variable):
    """ income * am_total_transit_time_walk_from_home_to_work"""
    _return_type="float32"

    travel_time = "am_total_transit_time_walk_from_home_to_work"
    
    def dependencies(self):
        return ["psrc_parcel.person_x_job." + self.travel_time,
                "household_income=person.disaggregate(household.income)"]

    def compute(self, dataset_pool):
        person_x_jobs = self.get_dataset()
        income = person_x_jobs.get_dataset(1).get_attribute_by_index("household_income", person_x_jobs.get_2d_index_of_dataset1())
        travel_time = person_x_jobs.get_attribute("am_total_transit_time_walk_from_home_to_work")
        return income * travel_time


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.person_x_job.income_and_am_total_transit_time_walk_from_home_to_work"
    
    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='persons',
            table_data={
                'person_id':array([1, 2, 3, 4, 5, 6]),
                'household_id':array([1, 1, 2, 3, 3, 3]),
                'member_id':array([1, 2, 1, 1, 2, 3]),
                },
        )
        storage.write_table(
            table_name='jobs',
            table_data={
                'job_id':array([1, 2, 3]),
                'zone_id':array([1, 2, 3]),
                },
        )
        storage.write_table(
            table_name='households',
            table_data={
                    'household_id': array([1,2,3,4,5]),
                    'zone_id': array([3, 1, 1, 1, 2]),
                    'income': array([100, 30, 200, 10, 30])
                },
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
                'am_total_transit_time_walk':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        person_x_job = dataset_pool.get_dataset('person_x_job')
        person_x_job.compute_variables(self.variable_name,
                                       dataset_pool=dataset_pool)
        values = person_x_job.get_attribute(self.variable_name)
        
        should_be = array([[100*1.1, 100*7.8, 100*2.2], 
                           [100*1.1,100*7.8, 100*2.2], 
                           [30*3.3, 30*0.5, 30*4.4], 
                           [200*3.3, 200*0.5, 200*4.4],
                           [200*3.3, 200*0.5, 200*4.4], 
                           [200*3.3, 200*0.5, 200*4.4]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()