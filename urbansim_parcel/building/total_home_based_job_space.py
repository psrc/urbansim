# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import minimum

class total_home_based_job_space(Variable):
    """ total number of home-based jobs a given building can accommodate.
    The job space of buildings is determined from sizes of the households living there 
    (for each household the minimum of number of members and 2 is taken). 
    An exception are multi-family buildings for which the job_space is 50.
    """
    
    def dependencies(self):
        return ["sum_minimum_persons_and_2=building.aggregate(urbansim_parcel.household.minimum_persons_and_2)",
                "urbansim.building.is_multi_family_residential",
                "urbansim_parcel.building.residential_units"]
                
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        job_space = buildings.get_attribute("sum_minimum_persons_and_2").copy()
        is_mf = buildings.get_attribute("is_multi_family_residential").astype("bool8")
        job_space[is_mf] = minimum(50, buildings.get_attribute("residential_units")[is_mf])
        return job_space

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
            "building":{"building_id":                array([1,2,3,4,5,6,7,8,9,10]),
                       "sum_minimum_persons_and_2":   array([1,1,2,2,1,2,2,1,2,2]),
                       "is_multi_family_residential": array([0,0,0,1,1,0,1,0,0,0], dtype="bool8"),
                        "residential_units":          array([2,4,1,100,49,4,10,7,6,0])
                },    
        }
        )
        
        should_be = array([1,1,2,50,49,2,10,1,2,2])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()