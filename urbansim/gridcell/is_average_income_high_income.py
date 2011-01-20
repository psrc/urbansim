# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class is_average_income_high_income(Variable):
    """Average income, as computed by dividing the sum of all household's incomes in the given cell by
    the total number of housholds in the cell"""

    _return_type="bool8"
    average_income = "average_income"

    def dependencies(self):
        return [my_attribute_label("average_income")]

    def compute(self, dataset_pool):
        hh = dataset_pool.get_dataset('household')
        if hh.mid_income_level < 0: # income levels not computed yet
            hh.calculate_income_levels(dataset_pool.get_dataset('urbansim_constant'))        
        return self.get_dataset().get_attribute("average_income") > hh.mid_income_level


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3]),
                    'average_income': array([150, 50, 250]),
                },
                'household':{
                    'household_id': array([1,2,3,4]),
                    'income': array([50, 100, 200, 300]),
                },
                'urbansim_constant':{
                    'low_income_fraction': array([.25]),
                    'mid_income_fraction': array([.25]),
                }
            }
        )
        
        should_be = array([0, 0, 1]) 
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()