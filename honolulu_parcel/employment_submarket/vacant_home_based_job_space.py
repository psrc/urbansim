# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_home_based_job_space(Variable):
    """ number of job spaces that is vacant/unoccupied"""
    
    def dependencies(self):
        return ["honolulu_parcel.employment_submarket.total_home_based_job_space",
                "honolulu_parcel.employment_submarket.number_of_home_based_jobs"
                ]

    def compute(self,  dataset_pool):
        emp_submarkets = self.get_dataset() 
        return clip_to_zero_if_needed(emp_submarkets.get_attribute("total_home_based_job_space") - 
                                      emp_submarkets.get_attribute("number_of_home_based_jobs"))
        
    def post_check(self,  values, dataset_pool=None):
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
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            "building":{"building_id":         array([1,2,3,4,5,6,7,8,9,10]),
                       "total_home_based_job_space": array([1,1,2,2,1,3,3,3,2,2]),
                       "number_of_home_based_jobs":  array([1,3,1,2,2,1,2,3,2,4])
                },                
        }
        )
        
        should_be = array([0, 0, 1, 0, 0, 2, 1, 0, 0, 0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()