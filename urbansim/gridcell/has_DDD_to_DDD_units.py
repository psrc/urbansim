# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_and

class has_DDD_to_DDD_units(Variable):
    """Boolean indicating whether or not the gridcell has one to DDD residential
    units"""

    def __init__(self, number1, number2):
        Variable.__init__(self)
        self.tnumber1 = number1
        self.tnumber2 = number2

    def dependencies(self):
        return [my_attribute_label("residential_units")]

    def compute(self, dataset_pool):
        return logical_and(self.get_dataset().get_attribute("residential_units")>=self.tnumber1,
                           self.get_dataset().get_attribute("residential_units")<=self.tnumber2)

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


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
                    "grid_id":array([1, 2, 3, 4]),
                    "residential_units":array([0, 1, 5, 10])
                }
            }
        )

        should_be = array([False, True, True, False])
        instance_name = "urbansim.gridcell.has_1_to_5_units"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()