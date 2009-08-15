# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import clip
from opus_core.variables.variable import Variable

class occupied_building_sqft_by_SSS_jobs(Variable):
    """Sum of jobs sqft per building.
    """

    _return_type="int32"

    def __init__(self, type):
        self.number_of_jobs = "number_of_%s_jobs" % type
        Variable.__init__(self)
        
    def dependencies(self):
        return ["urbansim_zone.building.%s" % self.number_of_jobs,
                "urbansim_zone.building.building_sqft_per_job"]

    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        return buildings.get_attribute(self.number_of_jobs) * buildings.get_attribute("building_sqft_per_job")



from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test(self):
        tester = VariableTester(
        __file__,
        package_order=['urbansim_parcel','urbansim'],
        test_data={
        "building":{"building_id":         array([1,2,3]),
                   "zone_id":              array([1,2,3]),
                   "building_type_id":     array([1,2,1]),
            },
        "building_sqft_per_job":{
                   "zone_id":              array([1,  1, 1,  2, 2, 2,  3, 3]),
                   "building_type_id":     array([1,  2, 3,  1, 2, 3,  1, 3]),
                   "building_sqft_per_job":array([100,50,200,80,60,500,20,10]),
            },  
         "job": {"job_id":      array([1,2,3,4, 5, 6, 7]),
                 "building_id": array([2,1,3,2, 1, 2, 3])
                           },
        'building_type':
            {
             "building_type_id":array([1,2,3]),
             "building_type_name":array(["commercial", "industrial", "residential"])
             },
                   }
                                )
        should_be = array([0,180,0])
        instance_name = 'urbansim_zone.building.occupied_building_sqft_by_industrial_jobs'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        should_be = array([200,0,40])
        instance_name = 'urbansim_zone.building.occupied_building_sqft_by_commercial_jobs'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()