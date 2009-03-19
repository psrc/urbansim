# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import zeros, logical_or, bool8

class work_full_time(Variable):
    """if a person is work full time"""

    def dependencies(self):
        return [my_attribute_label("primact")]
        
    def compute(self, dataset_pool):
        persons = self.get_dataset()
        full_time_primact = [1, 5, 6]
        results = zeros(persons.size(), dtype=bool8)
        for act in full_time_primact:
            results = logical_or(results,
                                 persons.get_attribute("primact")==act)
        return results
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from opus_core.resources import Resources
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person.work_full_time"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5]),
                    'household_id':array([1, 1, 3, 3, 3]),
                    'member_id':array([1,2,1,2,3]),
                    'primact':array([1,1,3,2,5])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'person':persons
                }, 
            dataset = 'person'
            )
            
        should_be = array([1, 1, 0, 0, 1])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()