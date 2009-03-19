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
                "zone":{
                          "zone_id":   array([1,2,3,4])
                          },
                "job":{
                        "zone_id":array([1, 1, 4, 4, 1, 2]),
                        "job_id":arange(1,7),
                }
            }
        )
        
        should_be = array([3, 1, 0, 2])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()