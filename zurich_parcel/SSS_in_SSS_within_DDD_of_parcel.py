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

class SSS_in_SSS_within_DDD_of_parcel(Variable):
    """total number of SSS in SSS within radius DDD of SSS"""
    _return_type = "int32"

    def __init__(self, what, wherein, radius):
        self.what = what
        self.wherein = wherein
        self.radius = radius
        Variable.__init__(self)
        fullname = self.name().rsplit('.',1)[1]
        fullname = fullname.replace("SSS", what, 1)
        fullname = fullname.replace("SSS", wherein, 1)
        fullname = fullname.replace("DDD", str(radius))
        self.fullname = fullname
    
    def dependencies(self):
        return [my_attribute_label("x_coord_sp"),
                my_attribute_label("y_coord_sp"),
                "urbansim_parcel.household.parcel_id",
                "urbansim_parcel.household.persons"
                ]

    def compute(self, dataset_pool):
        logger.start_block(name="compute variable %s" % self.fullname, verbose=False)
        
        logger.start_block(name="initialize datasets for %s" % self.fullname, verbose=False)
        parcels = self.get_dataset()
        arr = self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset(self.wherein), attribute_name=self.what)
        coords = column_stack( (parcels.get_attribute("x_coord_sp"), parcels.get_attribute("y_coord_sp")) )
        logger.end_block()
        
        logger.start_block(name="build KDTree for %s" % self.fullname, verbose=False)
        kd_tree = KDTree(coords, 100)
        logger.end_block()
        
        logger.start_block(name="compute for %s" % self.fullname)
        results = kd_tree.query_ball_tree(kd_tree, self.radius)
        logger.end_block()
        
        logger.start_block(name="sum results for %s" % self.fullname, verbose=False)
        return_values = array([arr[l].sum() for l in results])
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
