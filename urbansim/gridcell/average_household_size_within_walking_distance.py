# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32
from opus_core.logger import logger

class average_household_size_within_walking_distance(Variable):
    """Average household size within walking distance, computed by dividing the
    total population within walking distance by the number of household"""

    def dependencies(self):
        return [my_attribute_label("sum_population_within_walking_distance"),
                my_attribute_label("number_of_households_within_walking_distance")]

    def pre_check(self, dataset_pool):
        index = self.get_dataset().get_attribute("number_of_households_within_walking_distance")==0
        values = self.get_dataset().get_attribute("sum_population_within_walking_distance")[index]
        self.do_check("x == 0", values)

    def compute(self, dataset_pool):
        hhs_wwd = self.get_dataset().get_attribute("number_of_households_within_walking_distance")
        return ma.filled(self.get_dataset().get_attribute("sum_population_within_walking_distance")/
                      ma.masked_where(hhs_wwd == 0, hhs_wwd.astype(float32)),0.0)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", ma.filled(values,0.0))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        sum_population_within_walking_distance = array([0, 5000, 10000, 15000])
        number_of_households_within_walking_distance = array([0.0, 100.0, 300.0, 56.0])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'sum_population_within_walking_distance': sum_population_within_walking_distance,
                    'number_of_households_within_walking_distance': number_of_households_within_walking_distance
                }
            }
        )

        should_be = array([0, 50.0, 33.3333333, 267.8571429])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
