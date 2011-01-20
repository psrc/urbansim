# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
                "parcel":{                        
                          'parcel_id':array([1,2,3]),
                          "parcel_sqft":array([1000,200,1300]),
                          },
                 "building":{
                        'building_id':     array([1,   2,   3,   4,   5,   6,   7]),
                        'parcel_id':       array([1,   1,   2,   3,   3,   3,   3]),
                        "land_area":       array([600, 400, 100, 300, 150, 400, 400]),
                }
            }
        )
        
        should_be = array([0,100,50])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()