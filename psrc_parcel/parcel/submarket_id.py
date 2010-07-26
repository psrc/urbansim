# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from numpy import zeros
from psrc_parcel.datasets.submarket_dataset import SubmarketDataset, generate_unique_ids

class submarket_id(Variable):
    """ Return the submarket_id of parcel, as defined in the datasets/submarket_dataset.py
    """
    _return_type = "int32"
    
    def dependencies(self):
        return SubmarketDataset.submarket_definition

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        variable_names = [VariableName(v) for v in self.dependencies()]
        assert ds.get_dataset_name() == variable_names[0].get_dataset_name()
        short_names = [vn.get_alias() for vn in variable_names]
        return generate_unique_ids(ds, short_names)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
            'parcel_id'        :array([ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]),
            'large_area_id'    :array([11,11,21,21,31,31,11,11,21,21,31,31]),
            'land_use_type_id' :array([ 7,99, 7,99, 7,99, 0,99, 0, 7,99, 7]),
            },
        })
        should_be = array([1107, 1199, 2107, 2199, 3107, 3199, 1100, 1199, 2100, 2107, 3199, 3107])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
