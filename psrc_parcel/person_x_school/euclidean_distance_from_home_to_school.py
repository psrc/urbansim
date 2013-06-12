# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_euclidean_distance_variable import abstract_euclidean_distance_variable

class euclidean_distance_from_home_to_school(abstract_euclidean_distance_variable):
    agent_attribute = "urbansim_parcel.person.parcel_id"
    destination_attribute = "school.parcel_id"
    location_dataset_name = "parcel"
    coordinate_attributes = ("x_coord_sp", "y_coord_sp")

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array, sqrt
class Tests(opus_unittest.OpusTestCase):
        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            "person":{ 
                'person_id':   array([1, 2, 3, 4, 5, 6]),
                'household_id':array([1, 1, 5, 3, 3, 3]),
                'member_id':   array([1, 2, 1, 1, 2, 3]),
              #location_id:           6, 6,-1, 8, 8, 8
                }, 
             "school":{ 
                 'school_id': array([ 1, 2, 3, 4, 5]),
                 'parcel_id': array([-1, 9, 3, 1, 6]),
                },
             "household":{
                 'household_id':array([1, 2, 3, 4,  5]),
                 'building_id': array([6, 1, 8, 4, -1]),
                 },
            "building": {
                 'building_id': array([6, 1, 8, 4]),
                 'parcel_id': array([6, 1, 8, 4]),
                         
                },
             "parcel":{
                 'parcel_id':     array([1,  2,   3,   4,   5,   6,   7,   8,   9]),
                 'x_coord_sp':       array([1,  1,   1,   2,   2,   2,   3,   3,   3]),
                 'y_coord_sp':       array([1,  2,   3,   1,   2,   3,   1,   2,   3]),                
             },
         })
        M = euclidean_distance_from_home_to_school.default_value
        should_be = array([[M,   sqrt((2-3)**2+(3-3)**2), sqrt((2-1)**2+(3-3)**2), sqrt((2-1)**2+(3-1)**2), sqrt((2-2)**2+(3-3)**2)], 
                           [M,   sqrt((2-3)**2+(3-3)**2), sqrt((2-1)**2+(3-3)**2), sqrt((2-1)**2+(3-1)**2), sqrt((2-2)**2+(3-3)**2)], 
                           [M,   M,                           M,                           M,                           M], 
                           [M,   sqrt((3-3)**2+(2-3)**2), sqrt((3-1)**2+(2-3)**2), sqrt((3-1)**2+(2-1)**2), sqrt((3-2)**2+(2-3)**2)], 
                           [M,   sqrt((3-3)**2+(2-3)**2), sqrt((3-1)**2+(2-3)**2), sqrt((3-1)**2+(2-1)**2), sqrt((3-2)**2+(2-3)**2)], 
                           [M,   sqrt((3-3)**2+(2-3)**2), sqrt((3-1)**2+(2-3)**2), sqrt((3-1)**2+(2-1)**2), sqrt((3-2)**2+(2-3)**2)], 
                           ])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
