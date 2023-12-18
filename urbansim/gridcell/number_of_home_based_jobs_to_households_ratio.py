# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class number_of_home_based_jobs_to_households_ratio(Variable):
    """Average income, as computed by dividing the sum of all household's incomes in the given cell by
    the total number of housholds in the cell"""

    _return_type="float32"

    def dependencies(self):
        return [my_attribute_label("number_of_households"),
                my_attribute_label("number_of_home_based_jobs"),
                ]

    def compute(self, dataset_pool):
        nhhs = self.get_dataset().get_attribute("number_of_households")
        return ma.filled(self.get_dataset().get_attribute("number_of_home_based_jobs")/ 
                      ma.masked_where(nhhs == 0, nhhs.astype(float32)), 0.0)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    #EXAMPLE FOR TUTORIAL
    def test_my_inputs(self):
        number_of_hb_jobs = array([500, 10000, 500])
        number_of_households = array([300, 0, 500]) #specify the total number of households for each of three locations

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "number_of_home_based_jobs":number_of_hb_jobs,
                    "number_of_households":number_of_households
                }
            }
        )
        
        #if the dependent variables span different "directories", i.e. gridcell and household, then a "household" key
        #would also be added to this dictionary. the names of keys within MUST MATCH an already existing variable...
        #as a general rule, look at the dependencies for the actual variable code above, and each one should appear
        #somewhere in the compute_variable dictionary arguments, i.e. in this case, "sum_income" and "number_of_households"
        #the corresponding value name to the keys doesn't matter, in this case i chose them to be the same.
        
        should_be = array([1.666667, 0.0, 1.0]) #would be a 2-D array if it spanned more than one "directory"
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-5)


if __name__=='__main__':
    opus_unittest.main()