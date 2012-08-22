# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from numpy import zeros
from bayarea.datasets.area_permutation_dataset import AreaPermutationDataset, generate_unique_ids

class area_permutation_id(Variable):
    """ Return the area_permutation_id of parcel, as defined in the datasets/area_permutation_dataset.py
    """
    _return_type = "int32"
    
    def dependencies(self):
        return SubmarketDataset.subgroup_definition

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        variable_names = [VariableName(v) for v in self.dependencies()]
        assert ds.get_dataset_name() == variable_names[0].get_dataset_name()
        short_names = [vn.get_alias() for vn in variable_names]
        return generate_unique_ids(ds, short_names)[0]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

#===============================================================================
# from opus_core.tests import opus_unittest
# from numpy import array, int32
# from opus_core.tests.utils.variable_tester import VariableTester
# 
# class Tests(opus_unittest.OpusTestCase):
#    def test_my_inputs(self):
#        tester = VariableTester(
#            __file__,
#            package_order=['bayarea', 'urbansim_parcel', 'urbansim'],
#            test_data={
#            'parcel':
#            {
#            'parcel_id'       :array([ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]),
#            'pda_id'          :array([11,11,21,21,31,31,11,11,21,21,31,31]),
#            'tpp_id'          :array([ 7,9, 7,8, 7,4, 14,99, 6, 7,7, 9]),
#            'juris_id'        :array([ 101, 89, 101, 45, 101, 89, 29, 29, 2, 2, 2, 1]),
#            'county_id'        :array([ 1, 1, 3, 4, 1, 8, 2, 2, 1, 2, 2, 1]),
#            },
#        })
#        should_be = array([11071, 11991, 21072, 21992, 31071, 31992, 11001, 11991, 21002, 21072, 31992, 31071])
#                          
# 
#        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
# 
# if __name__=='__main__':
#    opus_unittest.main()
#===============================================================================
