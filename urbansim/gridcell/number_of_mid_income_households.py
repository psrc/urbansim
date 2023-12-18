# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label

class number_of_mid_income_households(Variable):
    """Number of mid-income households in this gridcell"""

    _return_type="int32"
    is_mid_income = "is_mid_income"

    def dependencies(self):
        return [attribute_label("household", self.is_mid_income), 
                attribute_label("household", "grid_id"), 
                my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, self.is_mid_income)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_full_tree(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    },
                'household':{
                    'household_id': array([1,2,3,4,5,6]),
                    'grid_id': array([1, 2, 3, 4, 2, 2]),
                    'income': array([1000, 5000, 3000, 10000, 1000, 8000]), # high income: > 5000
                    },
                'urbansim_constant':{
                    "low_income_fraction": array([.25]),
                    'mid_income_fraction': array([.3]),
                }
            }
        )
        
        should_be = array([0,1,1,0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()