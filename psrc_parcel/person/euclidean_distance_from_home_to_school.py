# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_euclidean_distance_non_interaction_variable import abstract_euclidean_distance_non_interaction_variable

class euclidean_distance_from_home_to_school(abstract_euclidean_distance_non_interaction_variable):
    origin_attribute = "urbansim_parcel.person.parcel_id"
    destination_attribute = "school_parcel_id = person.disaggregate(school.parcel_id)"
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
                'parcel_id':   array([6, 1, 8, 4, 1, -1]),
                'school_id':  array([ -1,3, 2, 3, 4, 3]),
                }, 
             "school":{ 
                 'school_id': array([ 1, 2, 3, 4, 5]),
                 'parcel_id': array([-1, 9, 3, 1, 6]),
                },
             "parcel":{
                 'parcel_id':     array([1,  2,   3,   4,   5,   6,   7,   8,   9]),
                 'x_coord_sp':    array([1,  1,   1,   2,   2,   2,   3,   3,   3]),
                 'y_coord_sp':    array([1,  2,   3,   1,   2,   3,   1,   2,   3]),                
             },
         })
        M = euclidean_distance_from_home_to_school.default_value
        should_be = array([M, sqrt((1-1)**2+(1-3)**2), sqrt((3-3)**2+(2-3)**2), sqrt((2-1)**2+(1-3)**2), 0, M])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
