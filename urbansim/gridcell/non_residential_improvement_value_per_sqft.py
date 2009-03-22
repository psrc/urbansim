# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32
from opus_core.logger import logger

class non_residential_improvement_value_per_sqft(Variable):
    """Average non-residential improvement value per non-residential sqft, computed by dividing the 
    total non-residential improvement value by non-residential sqft"""

    nonresidential_improvement_value = "nonresidential_improvement_value"
    non_residential_sqft = "non_residential_sqft"

    def dependencies(self):
        return [my_attribute_label(self.nonresidential_improvement_value), 
                my_attribute_label(self.non_residential_sqft)]

    def compute(self, dataset_pool):
        return self.safely_divide_two_attributes(self.nonresidential_improvement_value,
                                                 self.non_residential_sqft, -1.0)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", ma.filled(values,0.0))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        nonresidential_improvement_value = array([1000, 5000, 10000, 15000])
        non_residential_sqft = array([0.0, 10.0, 300.0, 56.0])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id":array([1,2,3,4]),
                    "nonresidential_improvement_value":nonresidential_improvement_value, 
                    "non_residential_sqft":non_residential_sqft
                }
            }
        )
        
        should_be = array([-1.0, 500.0, 10000/300.0, 15000/56.0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()