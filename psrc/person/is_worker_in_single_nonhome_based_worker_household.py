# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_and

class is_worker_in_single_nonhome_based_worker_household(Variable):
    """"""

    def dependencies(self):
        return [my_attribute_label("household_id"), 
                my_attribute_label("work_nonhome_based"), 
                "is_in_single_nonhome_based_worker_household = person.disaggregate(psrc.household.has_1_nonhome_based_workers)"]
        
    def compute(self, dataset_pool):
        persons = self.get_dataset()
        return logical_and(persons.get_attribute("work_nonhome_based"),
                           persons.get_attribute("is_in_single_nonhome_based_worker_household")) 
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person.is_worker_in_single_nonhome_based_worker_household"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5]),
                    'household_id':array([1, 1, 3, 3, 3]),
                    'member_id':array([1,2,1,2,3]),
                    'work_nonhome_based':array([0,1,1,1,0]),
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'household':{ 
                    'household_id':array([1,2,3])
                    },
                'person':persons
                },
            dataset = 'person'
            )
            
        should_be = array([0, 1, 0, 0, 0])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()