# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim_parcel.parcel.abstract_variable_within_radius_DDD_of_parcel import abstract_variable_within_radius_DDD_of_parcel

class number_of_private_schools_within_DDD_of_parcel(abstract_variable_within_radius_DDD_of_parcel):
    """Number of private schools within radius DDD of parcel"""
    _return_type = "int32"
    
    quantity = "psrc_parcel.parcel.number_of_private_schools"
    filter = "numpy.logical_or(parcel.aggregate(building.residential_units) > 0, psrc_parcel.parcel.number_of_private_schools > 0)"

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":  array([1,   2,    3, 4,5,6,7,8]),
                "x_coord_sp": array([1,   2,    3, 4,1,2,3,4]),
                "y_coord_sp": array([1,   1,    1, 1, 2,2,2,2 ]),
            },
            'school':
            {
                "school_id":array([1,2,3,4,5,6]),
                "parcel_id":array([1,2,4,5,7,8]),
                "public":   array([0,1,0,1,0,0])
             },
            'building':
            {
                "building_id":array([1,2,3,4,5,6,7,8]),
                "parcel_id":array([1,2,3,4,5,6,7,8]),
                "residential_units": array([1,2,1,5,7,3,1,6])
             },
        })
        should_be = array([1, 3, 4, 3, 2, 3, 3, 3])

        instance_name = 'psrc_parcel.parcel.number_of_private_schools_within_2_of_parcel'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        
    def test_filter(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":  array([1,   2,    3, 4,5,6,7,8]),
                "x_coord_sp": array([1,   2,    3, 4,1,2,3,4]),
                "y_coord_sp": array([1,   1,    1, 1, 2,2,2,2 ]),
            },
            'school':
            {
                "school_id":array([1,2,3,4,5,6]),
                "parcel_id":array([1,2,4,5,7,8]),
                "public":   array([0,1,0,1,0,0])
             },
            'building':
            {
                "building_id":array([1,2,3,4,5,6,7]),
                "parcel_id":array([1,2,3,4,5,7,8]),
                "residential_units": array([0,1,1,0,0,0,0])
             },
        })
        should_be = array([1, 3, 4, 3, 0, 0, 3, 3])

        instance_name = 'psrc_parcel.parcel.number_of_private_schools_within_2_of_parcel'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        

if __name__=='__main__':
    opus_unittest.main()
