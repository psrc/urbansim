# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import zeros
from numpy import array
from scipy.spatial import KDTree
from numpy import column_stack

class distance_to_SSS_dataset(Variable):
    """distance of parcel centroid to nearest SSS dataset point,
        id name = dataset name_id, e.g. for busstop dataset, busstop_id 
        x coordinate field name = point_x
        y coordinate field name = point_y"""
    _return_type = "int32"

    def __init__(self, points):
        self.points = points
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label("x_coord_sp"),
                my_attribute_label("y_coord_sp")]

    def compute(self, dataset_pool):
        loc = dataset_pool.get_dataset(self.points)
        self.add_and_solve_dependencies([self.points+".point_x", self.points+".point_y"], 
                                        dataset_pool=dataset_pool)
        pgcoords = column_stack( (loc.get_attribute("point_x"), loc.get_attribute("point_y")) )
        parcels = self.get_dataset()
        coords = column_stack( (parcels.get_attribute("x_coord_sp"), parcels.get_attribute("y_coord_sp")) )
        kd_tree = KDTree(pgcoords, 10)
        distances, indices = kd_tree.query(coords)
        return distances

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
                "parcel_id":  array([1,   2,    3,  4, 5]),
                "x_coord_sp": array([1,   2,    3,  3, 1 ]),
                "y_coord_sp": array([1,   1,    1,  2, 4 ]),
            },
            'busstop':
            {
             "busstop_id":array([1,2,3,4,5,6,7]),
             "point_x":array([1,2,3,2,2,1,3]),
             "point_y":array([1,1,1,2,2,1,3]),
             },
        })
        should_be = array([0, 0, 0, 1, 2])

        instance_name = 'urbansim_parcel.parcel.distance_to_busstop_dataset'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
