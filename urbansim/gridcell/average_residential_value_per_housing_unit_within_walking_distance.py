# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32
from opus_core.logger import logger

class average_residential_value_per_housing_unit_within_walking_distance(Variable):
    """Average residential value per housing units within walking distance, computed by dividing the 
    total residential value within walking distance by the number of residential units within walking distance """

    total_residential_value_within_walking_distance = "total_residential_value_within_walking_distance"
    housing_units_within_walking_distance = "residential_units_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.total_residential_value_within_walking_distance), 
                my_attribute_label(self.housing_units_within_walking_distance)]

    def compute(self, dataset_pool):
        return self.safely_divide_two_attributes(self.total_residential_value_within_walking_distance,
                                                   self.housing_units_within_walking_distance, -1.0)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", ma.filled(values,0.0))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        total_residential_value_within_walking_distance = array([1000, 5000, 10000, 15000])
        housing_units_within_walking_distance = array([0.0, 10.0, 300.0, 56.0])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id": array([1,2,3,4]),
                    "total_residential_value_within_walking_distance":total_residential_value_within_walking_distance, 
                    "residential_units_within_walking_distance":housing_units_within_walking_distance
                }
            }
        )
        
        should_be = array([-1.0, 500.0, 10000/300.0, 15000/56.0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
