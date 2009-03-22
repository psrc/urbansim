# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import zeros


class is_in_plan_type_group_SSS(Variable):
    """Returns a boolean indicating whether this gridcell's plan type group is
    of given name (by SSS)."""

    _return_type = "bool8"
    plan_type_id = "plan_type_id"

    def __init__(self, group):
        self.group = group
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("plan_type_group", "group_id"),
                attribute_label("plan_type_group", "name"),
                attribute_label("plan_type", "plan_type_id"),
                my_attribute_label("plan_type_id")]


    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        groups = dataset_pool.get_dataset('plan_type_group')
        group_id = groups.get_id_attribute()[groups.get_attribute("name")==self.group][0]
        devtypes = dataset.get_attribute("plan_type_id")
        types_in_group = dataset_pool.get_dataset('plan_type').get_types_for_group(group_id)
        result = zeros(dataset.size(),dtype=self._return_type)
        for type in types_in_group:
            result = result + (devtypes == type).astype(self._return_type)
        return result

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from opus_core.variables.attribute_box import AttributeBox
from numpy import array, arange
from numpy import ma

#emulates the plan type resource and implements the method we're interested in (are_in_group)
class mock_plantype(object):
    groups = {}
    groups[0] = array([1,2]) #define devtype 1 to be in group 1 and group 2
    groups[1] = array([2])
    groups[2] = array([3])
    def __init__(self, n):
        self.n = n

    def compute_variables_return_versions_and_final_value(self, name, *args, **kwargs):
        return ([0], array([1,2,3]))

    def get_types_for_group(self, group):
        ids = arange(self.n)+1
        is_group = array(map(lambda idx: group in self.groups[idx], range(self.size())), dtype="bool8")
        return ids[is_group]

    def size(self):
        return self.n

    def _get_attribute_box(self, name):
        return AttributeBox(self, None, name.get_alias())

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs( self ):
        tester = VariableTester(
            __file__,
            package_order=['urbansim', 'opus_core'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'plan_type_id': array([1, 3, 2, 3]),
                    },
                'plan_type_group':{
                    'name': array(["mixed_use", "high_density_residential"]),
                    'group_id': array([1,2]),
                }
            }
        )
        tester.dataset_pool._add_dataset('plan_type', mock_plantype(3))

        # Test variable 1
        should_be = array( [True, False, False, False] )
        instance_name1 = "urbansim.gridcell.is_in_plan_type_group_mixed_use"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name1)

        # Test variable 2
        should_be = array( [True, False, True, False] )
        instance_name2 = "urbansim.gridcell.is_in_plan_type_group_high_density_residential"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name2)


if __name__=='__main__':
    opus_unittest.main()