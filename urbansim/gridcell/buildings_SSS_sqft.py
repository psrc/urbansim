# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class buildings_SSS_sqft(Variable):
    """Sum of building space of given type across gridcells."""

    _return_type="float32"

    def __init__(self, type):
        self.sqft_variable = "%s_sqft" % type
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("building", self.sqft_variable),
                attribute_label("building", "grid_id")]

    def compute(self, dataset_pool):
        buildings = dataset_pool.get_dataset('building')
        type_sqft = buildings.get_attribute(self.sqft_variable)
        ds = self.get_dataset()
        return ds.sum_over_ids(buildings.get_attribute(ds.get_id_name()[0]), type_sqft)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        """Total number of commercial sqft of buildings.
        """
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id':array([1,2,3]),
                    },
                'building': {
                    'building_id':array([1,2,3,4,5,6]),
                    'building_type_id':array([1,2,1,2,1,1]),
                    'grid_id':array([2,3,1,1,2,1]),
                    'sqft':array([100, 350, 1000, 0, 430, 95])
                    },
                'building_type': {
                    'building_type_id':array([1,2]),
                    'name': array(['foo', 'commercial'])
                }
            }
        )

        should_be = array([0, 0, 350])
        instance_name = "urbansim.gridcell.buildings_commercial_sqft"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()