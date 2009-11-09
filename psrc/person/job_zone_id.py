# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class job_zone_id(Variable):
    """The zone_id of a person's job."""

    def dependencies(self):
        return [my_attribute_label("job_id"), 
                attribute_label("job","zone_id")]
        
    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().get_join_data(jobs, name="zone_id", 
                                                join_attribute="job_id")
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from opus_core.resources import Resources
from psrc.datasets.person_dataset import PersonDataset
from urbansim.datasets.job_dataset import JobDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person.job_zone_id"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5]),
                    'household_id':array([1, 1, 3, 3, 3]),
                    'member_id':array([1,2,1,2,3]),
                    'job_id':array([1,1,3,2,5])
                    },
            )

        jobs_table_name = 'jobs'
        storage.write_table(
                table_name=jobs_table_name,
                table_data={
                    'job_id':array([1,2,3,4]),
                    'zone_id':  array([5,6,7,8])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'job':{
                    'job_id':array([1,2,3,4]),
                    'zone_id':  array([5,6,7,8])
                    },
                'person':persons
                },
            dataset = 'person'
            )
            
        should_be = array([5, 5, 7, 6, -1])

        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()