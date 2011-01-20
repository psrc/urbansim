# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import float32, logical_and

class is_high_income_and_DDD_or_higher_percent_developed_within_walking(Variable):
    """"""

    _return_type="bool8"

    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number

    def dependencies(self):
        return [my_attribute_label("is_average_income_high_income"),
                my_attribute_label("percent_developed_within_walking_distance")] 

    def compute(self, dataset_pool):
        percent_developed = self.get_dataset().get_attribute("percent_developed_within_walking_distance")
        return logical_and(self.get_dataset().get_attribute("is_average_income_high_income"),
                           percent_developed >= self.tnumber)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    #EXAMPLE FOR TUTORIAL
    def test_my_inputs(self):
        high_income = array([1, 0, 1, 0]) #specify the total income for each of three locations
        percent_developed = array([49, 41, 80, 100])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "is_average_income_high_income":high_income,
                    "percent_developed_within_walking_distance":percent_developed
                }
            }
        )

        should_be = array([0, 0, 1, 0]) #would be a 2-D array if it spanned more than one "directory"
        instance_name = "urbansim.gridcell.is_high_income_and_50_or_higher_percent_developed_within_walking"    
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()