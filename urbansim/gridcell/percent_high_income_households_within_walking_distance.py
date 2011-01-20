# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class percent_high_income_households_within_walking_distance(Variable):
    """Computed by dividing the number_of_high_income_households_within_walking_distance
    by number_of_households_within_walking_distance"""
    _return_type="float32"
    number_of_high_income_households_within_walking_distance = "number_of_high_income_households_within_walking_distance"
    number_of_households_within_walking_distance ="number_of_households_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.number_of_high_income_households_within_walking_distance), 
                my_attribute_label(self.number_of_households_within_walking_distance)]

    def compute(self, dataset_pool):
        hh_wwd = self.get_dataset().get_attribute(self.number_of_households_within_walking_distance)
        return 100.0*ma.filled(self.get_dataset().get_attribute(self.number_of_high_income_households_within_walking_distance)/ 
                                             ma.masked_where(hh_wwd == 0, hh_wwd.astype(float32)), 0.0)

    def post_check(self, values, dataset_pool):
        self.do_check("0 <= x and x <= 100", ma.filled(values,0))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        number_of_high_income_households_within_walking_distance = array([0, 333, 500, 100])
        number_of_households_within_walking_distance = array([500, 501, 500, 0])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id": array([1,2,3,4]),
                    "number_of_high_income_households_within_walking_distance":number_of_high_income_households_within_walking_distance, 
                    "number_of_households_within_walking_distance":number_of_households_within_walking_distance
                }
            }
        )
        
        should_be = array([0.0, 333/501.0*100.0, 100.0, 0.0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()