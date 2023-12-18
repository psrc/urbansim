# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class number_of_persons(Variable):
    """number of persons in household."""
    
    def dependencies(self):
        return [my_attribute_label("household_id"), 
                attribute_label("person", "household_id"),
                ]
        
    def compute(self, dataset_pool):
        persons = dataset_pool.get_dataset('person')
        return self.get_dataset().sum_dataset_over_ids(persons, constant=1)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.number_of_persons"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5, 6]),
                    'household_id':array([1, 1, 2, 3, 3, 3]),
                    'member_id':array([1, 2, 1, 1, 2, 3]),
                    },
            )
        
        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'household':{
                    'household_id':array([2, 1, 3, 4])
                    },
                 'person':persons
                 },
            dataset = 'household'
            )
            
        should_be = array([1, 2, 3, 0])

        self.assertTrue(ma.allclose(values, should_be, rtol=1e-7),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()