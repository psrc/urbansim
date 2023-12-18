# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import zeros
from numpy import array
from scipy.spatial import KDTree
from numpy import column_stack

class households_within_DDD_of_parcel(Variable):
    """total number of households within radius DDD of parcel"""
    _return_type = "int32"

    def __init__(self, radius):
        self.radius = radius
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label("x_coord_sp"),
                my_attribute_label("y_coord_sp"),
                "urbansim_parcel.household.parcel_id"
                ]

    def compute(self, dataset_pool):
        parcels = self.get_dataset()
        arr = self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('household'), constant=1)
        coords = column_stack( (parcels.get_attribute("x_coord_sp"), parcels.get_attribute("y_coord_sp")) )
        kd_tree = KDTree(coords, 100)
        results = kd_tree.query_ball_tree(kd_tree, self.radius)
        return array([arr[l].sum() for l in results])

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "x_coord_sp": array([1,   2,    3 ]),
                "y_coord_sp": array([1,   1,    1 ]),
            },
            'household':
            {
                "household_id":array([1,2,3,4,5,6,7]),
                "building_id":array([1,2,3,4,5,6,7]),
             },
            'building':
            {
                "building_id":array([1,2,3,4,5,6,7]),
                "parcel_id":array([1,2,2,2,2,1,3]),
             },
        })
        should_be = array([6, 7, 5])

        instance_name = 'urbansim_parcel.parcel.households_within_1_of_parcel'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
