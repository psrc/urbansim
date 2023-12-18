# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import logical_and

class workerDDD(Variable):
    """if a person (worker) is workerDDD"""
   
    def __init__(self, workern):
        self.n = workern
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("member_id")]
        
    def compute(self, dataset_pool):
        persons = self.get_dataset()
        return logical_and(persons["member_id"] == self.n, persons["job_id"] > 0)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person.worker1"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5]),
                    'household_id':array([1, 1, 3, 3, 3]),
                    'member_id':array([1,2,1,2,3]),
                    'job_id':array([0,45,78,0,2])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'person':persons
                },
            dataset = 'person'
            )
            
        should_be = array([0, 0, 1, 0, 0])
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1e-7), 
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()