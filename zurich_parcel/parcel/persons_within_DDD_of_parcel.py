# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import zeros
from numpy import array
from scipy.spatial import KDTree
from numpy import column_stack
from opus_core.logger import logger

class persons_within_DDD_of_parcel(Variable):
    """total number of persons within radius DDD of parcel"""
    _return_type = "int32"

    def __init__(self, radius):
        self.radius = radius
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label("x_coord_sp"),
                my_attribute_label("y_coord_sp"),
                "urbansim_parcel.household.parcel_id",
                "urbansim_parcel.household.persons"
                ]

    def compute(self, dataset_pool):
        logger.start_block(name="compute variable persons_within_DDD_of_parcel with DDD=%s" % self.radius, verbose=False)

        logger.start_block(name="initialize datasets", verbose=False)
        parcels = self.get_dataset()
        arr = self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('household'), attribute_name="persons")
        coords = column_stack( (parcels.get_attribute("x_coord_sp"), parcels.get_attribute("y_coord_sp")) )
        logger.end_block()

        logger.start_block(name="build KDTree", verbose=False)
        kd_tree = KDTree(coords, 100)
        logger.end_block()

        logger.start_block(name="compute")
        results = kd_tree.query_ball_tree(kd_tree, self.radius)
        logger.end_block()

        logger.start_block(name="sum results", verbose=False)
        return_values = array(map(lambda l: arr[l].sum(), results))
        logger.end_block()

        logger.end_block()
        return return_values

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
                "parcel_id": array([1,   2,    3]),
                "x_coord_sp": array([1,   2,    3 ]),
                "y_coord_sp": array([1,   1,    1 ]),
            },
            'household':
            {
                "household_id":array([1,2,3,4,5,6,7]),
                "persons":array([3,5,2,2,2,1,3]),
                "building_id":array([1,2,3,4,5,6,7]),
             },
            'building':
            {
                "building_id":array([1,2,3,4,5,6,7]),
                "parcel_id":array([1,2,2,2,2,1,3]),
             },
        })
        should_be = array([15, 18, 14])

        instance_name = 'urbansim_parcel.parcel.persons_within_1_of_parcel'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
