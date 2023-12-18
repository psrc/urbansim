# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class average_income(Variable):
    """Average income, as computed by dividing the sum of all household's incomes in the given cell by
    the total number of households in the cell"""

    _return_type="float32"
    sum_income = "sum_income"
    number_of_households = "number_of_households"

    def dependencies(self):
        return [my_attribute_label(self.number_of_households),
                my_attribute_label(self.sum_income)]

    def compute(self, dataset_pool):
        nh = self.get_dataset().get_attribute(self.number_of_households)
        return ma.filled(self.get_dataset().get_attribute(self.sum_income)/ 
                                       ma.masked_where(nh == 0, nh.astype(float32)), 0.0)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    #EXAMPLE FOR TUTORIAL
    def test_my_inputs(self):
        sum_income = array([1000, 10000, 100000]) #specify the total income for each of three locations
        number_of_households = array([300, 20, 500]) #specify the total number of households for each of three locations

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{ 
                    'grid_id': array([1,2,3]),
                    'sum_income':sum_income, 
                    'number_of_households':number_of_households
                    }
                }
            )
            
        #if the dependent variables span different "directories", i.e. gridcell and household, then a "household" key
        #would also be added to this dictionary. the names of keys within MUST MATCH an already existing variable...
        #as a general rule, look at the dependencies for the actual variable code above, and each one should appear
        #somewhere in the compute_variable dictionary arguments, i.e. in this case, "sum_income" and "number_of_households"
        #the corresponding value name to the keys doesn't matter, in this case i chose them to be the same.
        #"dataset" is the name of the "directory" that this variable is located

        should_be = array([3.33333, 500.0, 200.0]) #would be a 2-D array if it spanned more than one "directory"
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-5)

    def test_for_err(self):
        sum_income = array([1000, 10000, 100000])
        number_of_households = array([1, 0, 500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{ 
                    'grid_id': array([1,2,3]),                    
                    'sum_income':sum_income, 
                    'number_of_households':number_of_households
                }
            }
        )
        
        should_be = array([1000.0, 0.0, 200.0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()