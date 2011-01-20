# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class job_sector_id(Variable):
    """The sector_id of a person's job."""

    def dependencies(self):
        return [my_attribute_label("job_id"), 
                attribute_label("job","sector_id")]
        
    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset("job")
        return self.get_dataset().get_join_data(jobs, name="sector_id", 
                                                join_attribute="job_id")
    

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person.job_sector_id"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='persons',
            table_data={
                'person_id':array([1, 2, 3, 4, 5]),
                'household_id':array([1, 1, 3, 3, 3]),
                'member_id':array([1,2,1,2,3]),
                'job_id':array([1,1,3,2,5])
                },
        )
        storage.write_table(
            table_name='jobs',
            table_data={
                'job_id':array([1,2,3,4]),
                'sector_id':  array([5,6,7,8])
                },
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        person = dataset_pool.get_dataset('person')
        person.compute_variables(self.variable_name,
                                 dataset_pool=dataset_pool)
        values = person.get_attribute(self.variable_name)
            
        should_be = array([5, 5, 7, 6, -1])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()