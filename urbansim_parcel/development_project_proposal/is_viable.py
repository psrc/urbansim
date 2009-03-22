# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
#from variable_functions import my_attribute_label
from numpy import bool8, zeros, bool8, logical_and

class is_viable(Variable):
    """whether the proposed development template is viable for a given parcel and its constraints
    """

    def dependencies(self):
        return ["urbansim_parcel.development_project_proposal.is_allowed_by_constraint",
                "urbansim_parcel.development_project_proposal.is_size_fit"
                 ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        return logical_and(proposals.get_attribute("is_allowed_by_constraint"),
                           proposals.get_attribute("is_size_fit"))

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel'],
            test_data={
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4]),
                "is_allowed_by_constraint": array([1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]),
                "is_size_fit":              array([0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1]),                
            }
            }
        )
        
        should_be = array([0, 1,  0, 0,  1, 0, 0, 0, 0, 1, 0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    