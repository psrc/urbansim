# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class ratio_vacant_industrial_sqft(Variable):
    """ vacant industrial_sqft / industrial_sqft. """ 
    _return_type="float32"
    vacant_industrial_sqft = "vacant_industrial_sqft"
    industrial_sqft = "industrial_sqft"

    def dependencies(self):
        return [my_attribute_label(self.vacant_industrial_sqft), 
                my_attribute_label(self.industrial_sqft)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.vacant_industrial_sqft)/ \
                self.get_dataset().get_attribute(self.industrial_sqft).astype(self._return_type)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0 and x <= 1", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "vacant_industrial_sqft":array([125, 10000, 0], dtype='float64'), 
                    "industrial_sqft":array([1995, 10000, 7500], dtype='float64')
                }
            }
        )
        
        should_be = array([0.06265664, 1.0, 0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()