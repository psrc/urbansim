# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label, create_dependency_name_with_number
from numpy import array, arange

class same_sector_employment_within_walking_distance(Variable):
    """Sum over c in cell.walking_radius, count of j in c.placed_jobs where j.sector = job.sector."""
        
    jobs_sector_id = "sector_id"
    
    def dependencies(self):
        return [attribute_label("job", self.jobs_sector_id)] + \
            create_dependency_name_with_number("sector_DDD_employment_within_walking_distance", "gridcell", range(1,19))
        
    def compute(self, dataset_pool):
        index = self.get_dataset().get_index(2)
        if index == None:
            index = arange(self.get_dataset().get_m())
        values = map(lambda x,y: self.get_dataset().get_dataset(2).get_attribute_by_index("sector_"+str(int(x))+"_employment_within_walking_distance",y), 
            self.get_dataset().get_attribute_of_dataset(self.jobs_sector_id), index)
        return array(values)
        

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job_x_gridcell.same_sector_employment_within_walking_distance"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='jobs',
            table_data={
                'job_id': array([1,2,3,4]),
                'sector_id': array([2,1,2,3]),
                'grid_id': array([1,2, 3, 4]),
            }
        )
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "walking_distance_circle_radius": array([150]),
                'cell_size': array([150]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)
        job_x_gridcell = dataset_pool.get_dataset('job_x_gridcell')
        job_x_gridcell.compute_variables(self.variable_name, 
                                         dataset_pool=dataset_pool)
        values = job_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([4,3,4,3])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()