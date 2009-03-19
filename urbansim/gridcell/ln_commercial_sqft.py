# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_commercial_sqft(Variable):
    """Natural log of the commercial_sqft for this gridcell"""
        
    _return_type="float32"
    commercial_sqft = "commercial_sqft"

    def dependencies(self):
        return [my_attribute_label(self.commercial_sqft)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.commercial_sqft))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        """Log of the amount of commercial space on cell.[ln_bounded(c.commercial_sqft )]
        """
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1, 2, 3]),
                    "commercial_sqft":array([1, 1000, 20])
                }
            } 
        )
        
        should_be = array([0.0, 6.907755, 2.995732])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()