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
                "zone":{
                    "zone_id":array([1,2,3,4])},
                "household":{
                            "zone_id":array([1, 1, 1, 4, 4, 4, 1, 2, 2, 2]),
                            "household_id":arange(1,11),
                            "income":array([10, 1, 7, 2, 3, 5, 4, 9, 8, 6]),
                }
            }
        )

        ## due to extrapolation
        ## from opus_core.variables.functions import scoreatpercentile
        ## scoreatpercentile(array([10, 1, 7, 2, 3, 5, 4, 9, 8, 6]), 25) == 3.25
        should_be = array([1, 0, 0, 2])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
