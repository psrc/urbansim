# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import where

class number_of_nonhome_based_workers(Variable):
    """The number of nonhome workers in household."""
    
    def dependencies(self):
        return [my_attribute_label("household_id"), 
                attribute_label("person", "work_nonhome_based"),
                attribute_label("person", "household_id"),
                ]
        
    def compute(self, dataset_pool):
        persons = dataset_pool.get_dataset('person')
        household_ids = persons.get_attribute("household_id")
        work_nonhome_based = persons.get_attribute("work_nonhome_based")
        false_results = self.get_dataset().sum_over_ids(household_ids, work_nonhome_based)

        #FOR 1 NHB WRKR SUBMODEL:
        #false_results[where(false_results==0)] = -99
        #false_results[where(false_results==1)] = 0
        #false_results[where(false_results==2)] = 1
        #false_results[where(false_results==-99)] = 2
        
        #FOR 2 NHB WRKR SUBMODEL:
        #false_results[where(false_results==0)] = -99
        #false_results[where(false_results==1)] = 1
        #false_results[where(false_results==2)] = 0
        #false_results[where(false_results==-99)] = 2
        
        return false_results
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.number_of_nonhome_based_workers"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1,  2,  3,  4,  5,  6]),
                    'household_id':array([1,  1,  2,  3,  3,  3]),
                    'member_id':array([1,  2,  1,  1,  2,  3]),
                    'work_nonhome_based':array([1,  0,  0,  1,  0,  1]),
                    },
            )
        
        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'household':{
                    'household_id':array([2, 1, 3, 4])
                    },
                'person':persons
                }, 
            dataset = 'household'
            )
            
        should_be = array([0, 1, 2, 0])

        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()