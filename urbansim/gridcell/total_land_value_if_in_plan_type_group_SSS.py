# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class total_land_value_if_in_plan_type_group_SSS(Variable):
    """Sum of land values of locations if in plan_type_group SSS, 0 otherwise."""

    def __init__(self, group):
        self.group = group
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label("is_in_plan_type_group_%s" % self.group), 
                my_attribute_label("total_land_value")]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("is_in_plan_type_group_%s" % self.group) * \
               self.get_dataset().get_attribute("total_land_value")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        total_land_value = array([100, 200, 300])
        is_in_plan_type_group_residential = array([1, 0, 1])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "total_land_value":total_land_value, 
                    "is_in_plan_type_group_residential":is_in_plan_type_group_residential
                }
            }
        )
        
        should_be = array([100, 0, 300])
        instance_name = "urbansim.gridcell.total_land_value_if_in_plan_type_group_residential"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()