# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_young(Variable):
    """Is the head of the household young. """
    age_of_head = "age_of_head"
    
    def dependencies(self):
        return [my_attribute_label(self.age_of_head)]
            
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.age_of_head) <= \
            dataset_pool.get_dataset('urbansim_constant')["young_age"]


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.is_young"

    def test_my_inputs( self ):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4]),
                'age_of_head': array([12, 20, 25, 30]),
            }
        )
        
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                'young_age': array([25]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household = dataset_pool.get_dataset('household')
        household.compute_variables(self.variable_name, 
                                    dataset_pool=dataset_pool)
        values = household.get_attribute(self.variable_name)
        
        should_be = array( [1,1,1,0] )
        
        self.assert_(ma.allequal(values, should_be,), 
                     msg="Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()