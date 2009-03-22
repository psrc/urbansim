# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import ma

class n_recent_buildings(Variable):
    """Number of buildings per each gridcell built in the last
    N years, where N is the values of the recent_years field of the
    uransim_constants table.
    """

    _return_type="int32"

    def dependencies(self):
        return [attribute_label("building", "building_age"), attribute_label("building", "grid_id")]

    def compute(self, dataset_pool):
        recent_years = dataset_pool.get_dataset('urbansim_constant')["recent_years"]
        buildings = dataset_pool.get_dataset('building')
        age = buildings.get_attribute("building_age")
        is_built_recently = ma.filled(age,recent_years+1) <= recent_years
        return self.get_dataset().sum_over_ids(buildings.get_attribute("grid_id"), is_built_recently)

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        age =     array([20, 2, 0, 3, 1, 30])
        grid_id = array([1,  1,  2, 3, 1,  2])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id": array([1,2,3])
                    },
                "building":{
                    "building_id": array([1,2,3,4,5,6]),
                    "grid_id": grid_id,
                    "building_age": age
                    },
                "urbansim_constant":{
                    "recent_years": array([3])
                }
            }
        )

        should_be = array([2, 1, 1])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()