# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class sum_income(Variable):
    """Sum of all income in a gridcell, by summing the incomes of each household in the gridcell"""

    _return_type="int64"
    hh_income = "income"

    def dependencies(self):
        return [my_attribute_label("grid_id"), 
                attribute_label("household", self.hh_income), 
                attribute_label("household", "grid_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, self.hh_income)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        gridcell_grid_id = array([1, 2, 3])
        hh_income = array([1000, 5000, 10000, 2000])
        household_grid_id = array([2, 3, 1, 2])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":gridcell_grid_id
                    }, 
                "household":{ 
                    "household_id":array([1,2,3,4]),
                    "grid_id":household_grid_id, 
                    "income":hh_income
                } 
            }
        )
        
        should_be = array([10000, 3000, 5000])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
