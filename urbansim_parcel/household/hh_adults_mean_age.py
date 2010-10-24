# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, array
from opus_core import ndimage
from opus_core.variables.variable import Variable

class hh_adults_mean_age(Variable):
    """Average age of adults in a household. An adult is a person of age >= 18."""

    _return_type="float32"
    
    def dependencies(self):
        return ["is_adult = person.age >= 18", "person.household_id"]

    def compute(self,  dataset_pool):
        persons = dataset_pool.get_dataset('person')
        hhs = self.get_dataset()
        where_adult = where(persons.get_attribute('is_adult'))[0]
        age = persons.get_attribute('age')
        return array(ndimage.mean(age[where_adult], labels=persons.get_attribute('household_id')[where_adult],
                              index=hhs.get_id_attribute()))
    
from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={            
            'household':
            {
                'household_id': arange(5)+1,
            },
            'person': {
                 'person_id': arange(13),
                 'household_id': array([2,  2,   2, 3,  3,  1,  1,  1, 1, 4, 5,  5, 5]),     
                 'age':          array([35, 40, 10, 18, 19, 40, 42, 0, 5, 25, 68,69,24])
                       }
            }
        )
        
        should_be = array([(40+42)/2., (35+40)/2., (18+19)/2.,  25, (68+69+24)/3.])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    