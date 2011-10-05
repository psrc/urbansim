# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_and

class is_income_DDD(Variable):
    """ Is this household income in the range specified by the income type DDD.
        This range is specified in urbansim_constant by the fuction get_income_range_for_type. """
    income = "income"
    
    def __init__(self, number):
        self.tnumber = number
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.income)]

    def compute(self, dataset_pool):
        min_income, max_income = dataset_pool.get_dataset('urbansim_constant').get_income_range_for_type(self.tnumber)
        return logical_and(self.get_dataset().get_attribute(self.income) >= min_income, 
                           self.get_dataset().get_attribute(self.income) < max_income)

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)
        

from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester


class Tests(opus_unittest.OpusTestCase):
        
    def test_internal_categories( self ):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'household': {
                    'household_id': array([1, 2, 3, 4]),
                    'income': array([45000, 50000, 75000, 100000]),
                    },
                'urbansim_constant': {
                       'id': array([1])               
                    }
            }
        )    
        should_be = array( [1, 1, 0, 0] )
        instance_name = "urbansim.household.is_income_3"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        
    def test_external_categories( self ):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'household': {
                    'household_id': array([1, 2, 3, 4]),
                    'income': array([45, 50, 75, 10]),
                    },
                'urbansim_constant': {
                       'income_category_1_min': array([0]),
                       'income_category_1_max': array([30]),      
                       'income_category_2_min': array([31]),
                       'income_category_2_max': array([60]),           
                    }
            }
        )    
        tester.test_is_equal_for_family_variable(self, array( [1, 1, 0, 0] ), "urbansim.household.is_income_2")
        tester.test_is_equal_for_family_variable(self, array( [0, 0, 0, 1] ), "urbansim.household.is_income_1")
        tester.test_is_equal_for_family_variable(self, array( [0, 0, 0, 0] ), "urbansim.household.is_income_3") # internal category


if __name__=='__main__':
    opus_unittest.main()