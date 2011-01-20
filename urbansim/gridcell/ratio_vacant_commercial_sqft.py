# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class ratio_vacant_commercial_sqft(Variable):
    """ vacant commercial_sqft / commercial_sqft. """ 
    _return_type="float32"
    vacant_commercial_sqft = "vacant_commercial_sqft"
    commercial_sqft = "commercial_sqft"

    def dependencies(self):
        return [my_attribute_label(self.vacant_commercial_sqft), 
                my_attribute_label(self.commercial_sqft)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.vacant_commercial_sqft)/ \
                self.get_dataset().get_attribute(self.commercial_sqft).astype(self._return_type)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0 and x <= 1", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        vacant_commercial_sqft = array([125, 10000, 0])
        commercial_sqft = array([1995, 10000, 7500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "vacant_commercial_sqft":vacant_commercial_sqft, 
                    "commercial_sqft":commercial_sqft
                }
            }
        )
        
        should_be = array([0.06265664, 1.0, 0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()