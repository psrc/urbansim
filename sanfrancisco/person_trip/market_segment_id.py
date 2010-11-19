# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from numpy import zeros
from sanfrancisco.datasets.market_segment_dataset import MarketSegmentDataset, generate_unique_ids

class market_segment_id(Variable):
    """
    """
    _return_type = "int32"
    
    def dependencies(self):
        return MarketSegmentDataset.subgroup_definition

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        variable_names = [VariableName(v) for v in self.dependencies()]
        assert ds.get_dataset_name() == variable_names[0].get_dataset_name()
        short_names = [vn.get_alias() for vn in variable_names]
        return generate_unique_ids(ds, short_names)[0]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco', 'urbansim_parcel', 'urbansim'],
            test_data={
            'person_trip':
            {
            'person_trip_id':    array([ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]),
            'income_break':    array([101,11,21,201,31,31,101,11,201,21,31,31]),
            'mode_id'       :    array([  7, 9, 7, 99, 7,99,  0,99, 0, 7,99, 7]),
            'time_period'   :    array([  1, 3, 4,100, 4, 9,  0, 9, 0, 2,100,3]),
            },
        })
        should_be = array([10107001, 1109003, 2107004, 20199100, 3107004, 3199009, 10100000, 1199009, 20100000, 2107002, 3199100, 3107003])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
