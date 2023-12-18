# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import float32

class average_income_when_has_DDD_units(Variable):
    """Average income, as computed by dividing the sum of all household's incomes in the given cell by
    the total number of housholds in the cell"""

    _return_type="float32"

    def __init__(self, number1):
        self.tnumber1 = number1
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("average_income"),
                my_attribute_label("has_%s_units" % self.tnumber1)]

    def compute(self, dataset_pool):
        
        return self.get_dataset().get_attribute("average_income") * \
               self.get_dataset().get_attribute("has_%s_units" % self.tnumber1)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    instance_name = "urbansim.gridcell.average_income_when_has_1_units"
    #EXAMPLE FOR TUTORIAL
    def test_my_inputs(self):
        avg_income = array([1000, 10000, 100000]) #specify the total income for each of three locations
        units = array([3, 1, 10]) #specify the total number of households for each of three locations

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id": array([1,2,3]),
                    "average_income":avg_income, 
                    "residential_units":units
                }
            } 
        )
        #if the dependent variables span different "directories", i.e. gridcell and household, then a "household" key
        #would also be added to this dictionary. the names of keys within MUST MATCH an already existing variable...
        #as a general rule, look at the dependencies for the actual variable code above, and each one should appear
        #somewhere in the compute_variable dictionary arguments, i.e. in this case, "sum_income" and "number_of_households"
        #the corresponding value name to the keys doesn't matter, in this case i chose them to be the same.
        #"dataset" is the name of the "directory" that this variable is located
 
        should_be = array([0.0, 10000.0, 0.0]) #would be a 2-D array if it spanned more than one "directory"
        tester.test_is_equal_for_family_variable(self, should_be, self.instance_name)

    def test_for_err(self):
        avg_income = array([1000, 10000, 100000])
        units = array([1, 0, 500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id": array([1,2,3]),
                    "average_income":avg_income, 
                    "residential_units":units
                }
            }
        )
        
        should_be = array([1000.0, 0.0, 0.0])
        tester.test_is_equal_for_family_variable(self, should_be, self.instance_name)


if __name__=='__main__':
    opus_unittest.main()