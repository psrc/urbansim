# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class home_district_is_same_as_workplace_district(Variable):
    """returns binary 1 or 0 depending whether or not the districts of 
       a person's home and workplace are the same
    """

    def dependencies(self):
        return ["district_id = building.disaggregate(zone.district_id, intermediates=[parcel])",
                "home_district  = household.disaggregate(building.district_id)",
                "home_district = person.disaggregate(household.home_district)",
                "workplace_district = job.disaggregate(building.district_id)",
            ]

    def compute(self, dataset_pool):
        return self.get_dataset().is_same_as("home_district", 
                                             "workplace_district")

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import arange, array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc', 'urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            "building":{ 
                 "building_id": array([1,2,3,4]),
                 "district_id":   array([1,3,1,2])
                           }, 
            "household":{ 
                 "household_id":array([1,2,3,4,5,6]),
                 "building_id": array([1,1,3,2,4,2])
                              },
            "person":{
                 "person_id":    array([1,2,3,4,5,6,7,8]),
                 "household_id": array([1,2,2,2,3,4,5,6]),
                #"area_type":    array([1,1,1,1,1,3,2,3])
                 },
            "job":{
                 "job_id":      array([1,2,3,4,5]),
                 "building_id": array([1,3,4,1,4]),
                #"area_type":   array([1,1,2,1,2])
                       }
             })
        should_be = array([[1,1,0,1,0],
                           [1,1,0,1,0],
                           [1,1,0,1,0],
                           [1,1,0,1,0],
                           
                           [1,1,0,1,0],
                           [0,0,0,0,0],
                           [0,0,1,0,1],
                           [0,0,0,0,0],
                       ])
                            
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)



if __name__=='__main__':
    opus_unittest.main()
