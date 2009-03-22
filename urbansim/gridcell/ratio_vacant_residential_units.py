# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class ratio_vacant_residential_units(Variable):
    """ vacant residential_units / residential_units. """ 
    _return_type="float32"
    vacant_residential_units = "vacant_residential_units"
    residential_units = "residential_units"

    def dependencies(self):
        return [my_attribute_label(self.vacant_residential_units), 
                my_attribute_label(self.residential_units)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.vacant_residential_units)/ \
                self.get_dataset().get_attribute(self.residential_units).astype(self._return_type)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0 and x <= 1", values)
        

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        vacant_residential_units = array([125, 10000, 0])
        residential_units = array([1995, 10000, 7500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "vacant_residential_units":vacant_residential_units, 
                    "residential_units":residential_units
                }
            }
        )
        
        should_be = array([0.06265664, 1.0, 0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()