# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import ma
from opus_core.misc import safe_array_divide
from opus_core.simulation_state import SimulationState

class job_capacity_computed_if_necessary(Variable):
    """get job_capacity either from base_year job_capacity or computed from non_residential_sqft / building_sqft_per_job for new buildings
    """
    
    _return_type = "int32"
    
    def dependencies(self):
        return ["urbansim_parcel.building.non_residential_sqft",
                "urbansim_parcel.building.building_sqft_per_job",
                ]

    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        non_residential_sqft = buildings.get_attribute("non_residential_sqft")
        building_sqft_per_job = buildings.get_attribute("building_sqft_per_job")
        job_spaces = safe_array_divide(buildings['non_residential_sqft'], buildings['building_sqft_per_job'])
        ## only do this when job_capacity and year_built are primary attributes of buildings
        known_names = buildings.get_known_attribute_names()
        if 'job_capacity' in known_names and 'year_built' in known_names:
            self.add_and_solve_dependencies(["building.job_capacity", "building.year_built"],
                                                dataset_pool=dataset_pool)
            base_year = SimulationState().get_start_time()
            job_spaces[buildings['year_built']<=base_year] = buildings['job_capacity'][buildings['year_built']<=base_year]
        return job_spaces

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel','urbansim'],
            test_data={
            "building":{"building_id":         array([1,2,3,4,5,6,7,8,9,10]),
                       "zone_id":              array([1,1,2,2,1,3,3,3,2,2]),
                       "building_type_id":     array([1,3,1,2,2,1,2,3,2,4]),
                       "job_capacity":         array([0,1,2,0,0,1,2,2,0,5])*10,
                       "year_built":          array([-1,0,1,1,1,2,2,2,0,0])+2000,
                       "non_residential_sqft": array([1,2,2,1,7,0,3,5,4,6])*1000,
                },
            "building_sqft_per_job":{
                       "zone_id":              array([1,  1, 1,  2, 2, 2,  3, 3]),
                       "building_type_id":     array([1,  2, 3,  1, 2, 3,  1, 3]),
                       "building_sqft_per_job":array([100,50,200,80,60,500,20,10]),
                },                
        }
        )
        SimulationState().set_start_time(2000)
        # mean over "building_sqft_per_job" is 127.5
        should_be = array([0, 10, 2000/80., 1000/60., 7000/50., 0/200, 3000/127.5 ,
                           5000/10., 0, 50]).astype("int32")
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
