# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_distance_to_SSS_dataset import abstract_distance_to_SSS_dataset

class distance_to_SSS_dataset(abstract_distance_to_SSS_dataset):
    """distance of parcel centroid to nearest SSS dataset point,
        id name = dataset name_id, e.g. for busstop dataset, busstop_id 
        x coordinate field name = point_x
        y coordinate field name = point_y"""
    _return_type = "int32"
    dataset_x_coord = "point_x"
    dataset_y_coord = "point_y"
    my_x_coord = "x_coord_sp"
    my_y_coord = "y_coord_sp"
    package = "urbansim_parcel"
    from_dataset = "parcel"


from opus_core.tests import opus_unittest
from numpy import array
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
