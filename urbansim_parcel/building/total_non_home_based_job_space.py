# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from numpy import ma

class total_non_home_based_job_space(Variable):
    """ total number of non-home-based jobs a given building can accommodate"""
    
    _return_type = "int32"
    
    def dependencies(self):
        return ["urbansim_parcel.building.non_residential_sqft",
                "urbansim_parcel.building.building_sqft_per_job",
                ]

    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        non_residential_sqft = buildings.get_attribute("non_residential_sqft")
        building_sqft_per_job = buildings.get_attribute("building_sqft_per_job")
        return ma.filled(ma.masked_where(building_sqft_per_job==0, non_residential_sqft / building_sqft_per_job), 0)

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            "building":{"building_id":         array([1,2,3,4,5,6,7,8,9,10]),
                       "zone_id":              array([1,1,2,2,1,3,3,3,2,2]),
                       "building_type_id":     array([1,3,1,2,2,1,2,3,2,4]),
                       "non_residential_sqft": array([1,2,2,1,7,0,3,5,4,6])*1000,
                },
            "building_sqft_per_job":{
                       "zone_id":              array([1,  1, 1,  2, 2, 2,  3, 3]),
                       "building_type_id":     array([1,  2, 3,  1, 2, 3,  1, 3]),
                       "building_sqft_per_job":array([100,50,200,80,60,500,20,10]),
                },                
        }
        )
        # mean over "building_sqft_per_job" is 127.5
        should_be = array([1000/100., 2000/200., 2000/80., 1000/60., 7000/50., 0/200, 3000/127.5 ,
                           5000/10., 4000/60., 6000/127.5]).astype("int32")
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()