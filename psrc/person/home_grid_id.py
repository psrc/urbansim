# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class home_grid_id(Variable):
    '''The grid_id of a person's residence.'''

    def dependencies(self):
        return [my_attribute_label('household_id'), 
                'psrc.household.grid_id']
        
    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().get_join_data(households, name='grid_id')
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = 'psrc.person.home_grid_id'
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5]),
                    'household_id':array([1, 1, 3, 3, 3]),
                    'member_id':array([1,2,1,2,3])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'household':{ 
                    'household_id':array([1,2,3]),
                    'grid_id':array([9, 9, 7])
                    },
                'person':persons
                }, 
            dataset = 'person'
            )
            
        should_be = array([9, 9, 7, 7, 7])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()