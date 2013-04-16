# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim_parcel.parcel.distance_to_SSS_dataset import distance_to_SSS_dataset

class distance_to_school(distance_to_SSS_dataset):
    """distance of parcel centroid to nearest school"""

    _return_type = "float32"
    dataset_x_coord = "school.disaggregate(parcel.x_coord_sp)"
    dataset_y_coord = "school.disaggregate(parcel.y_coord_sp)"
    to_dataset = "school"
    
    def __init__(self):
        Variable.__init__(self)
        
from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":  array([1,   2,    3,  4, 5, 7, 8 ]),
                "x_coord_sp": array([1,   2,    3,  3, 1, 2, 3 ]),
                "y_coord_sp": array([1,   1,    1,  2, 4, 2, 3 ]),
            },
            'school':
            {
             "school_id": array([1, 2, 3, 4, 5, 6, 7]),
             "parcel_id": array([1, 2, 3, 7, 7, 1, 8])
             },
        })
        should_be = array([0, 0, 0, 1, 2.23607, 0, 0])

        instance_name = 'psrc_parcel.parcel.distance_to_school'
        tester.test_is_close_for_family_variable(self, should_be, instance_name, rtol=1e-5)

if __name__=='__main__':
    opus_unittest.main()
