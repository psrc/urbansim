# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
import re

class is_work_place_in_county_DDD(Variable):
    """Returns a boolean indicating if the person's work place is in DDD coded county
    (with and without leading 0) """
    
    def __init__(self, number):
        self.number = number
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("work_place_county")]

    def compute(self, dataset_pool):
        counties = self.get_dataset().get_attribute("work_place_county")
        pattern = re.compile('^0*'+str(self.number))
        return [pattern.match(county) != None for county in counties]

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person.is_work_place_in_county_033"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5]),
                    'household_id':array([1, 1, 3, 3, 3]),
                    'member_id':array([1,2,1,2,3]),
                    'work_place_county':array(['033','061','035','033','033'])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            data_dictionary = {
                'person':persons
                }, 
            dataset = 'person'
            )
            
        should_be = array([True, False, False, True, True])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()