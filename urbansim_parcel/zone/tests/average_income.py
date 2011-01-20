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
                            "zone_id":array([1, 1, 4, 4, 1, 2]),
                            "household_id":arange(1,7),
                            "income":array([10, 0, 7, 2, 3, 5]),
                }
            }
        )
        
        should_be = array([13.0/3.0, 5.0, 0, 9.0/2.0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

    def test_finding_ids(self):
        # similar test, but we don't put the zone id in the household dataset -- instead
        # it has to be computed by finding the building with the household in it, then the
        # zone with that building
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
                "zone": {"zone_id": arange(1,4)},
                "building": {"building_id":  arange(1,6),
                           "zone_id": array([1, 3, 1, 2, 2])},
                "household":{
                            "building_id": array([1, 1, 4, 4, 1, 5, 3]),
                            "household_id": arange(1,8),
                            "income": array([10, 0, 7, 2, 3, 5, 20]),
                }
            }
        )
        should_be = array([33.0/4.0, 14.0/3.0, 0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
