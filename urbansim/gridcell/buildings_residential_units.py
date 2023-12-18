# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class buildings_residential_units(Variable):
    """Sum of residential units  across gridcells."""

    _return_type="float32"
    residential_units = "residential_units"

    def dependencies(self):
        return [attribute_label("building", "residential_units" ),
                attribute_label("building", "grid_id")]

    def compute(self, dataset_pool):
        buildings = dataset_pool.get_dataset('building')
        units = buildings.get_attribute("residential_units")
        return self.get_dataset().sum_over_ids(buildings.get_attribute("grid_id"), units)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        """Total number of residential units from single family buildings.
        """
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id':array([1,2,3]),
                    },
                'building': {
                    'building_id':   array([1,2,3,4,5,6]),
                    'building_type': array([1,2,1,2,1,1]),
                    'grid_id':       array([2,3,1,1,2,1]),
                    'residential_units': array([100, 350, 1000, 0, 430, 95])
                    },
                'building_type': {
                    'building_type_id':array([1,2]),
                    'name': array(['foo', 'single_family'])
                }
            }
        )

        should_be = array([1095, 530, 350])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()