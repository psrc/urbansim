# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 


from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
                "building":{"building_id":array([1,2,3,4,5]),
                            "parcel_id":  array([2,1,2,3,1]),
                            },
                "household":{
                            "building_id":array([1,1,2,3,7]),
                            "household_id":arange(1,6),
                }
            }
        )
        
        should_be = array([2, 2, 1, 2, -1])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()