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
                       "building":{
                                   "building_id": array([1,2,3,4,5,6]),
                                   },
                       "household":{
                          "household_id": arange(1,7),
                          "building_id":array([1,2,2,2,1,5]),
                          "persons":array([2,1,1,5,3,7]),
                          }
            }
        )
        
        should_be = array([5,7,0,0,7,0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()