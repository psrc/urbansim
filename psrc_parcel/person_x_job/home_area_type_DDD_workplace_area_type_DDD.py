# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable

class home_area_type_DDD_workplace_area_type_DDD(Variable):
    """returns binary 1 or 0 depending whether or not the area types of 
       a person's home and workplace are of specified area_type_id respectively
    """
    def __init__(self, home_area_type, workplace_area_type):
        self.home_area_type = home_area_type
        self.workplace_area_type = workplace_area_type
        Variable.__init__(self)

    def dependencies(self):
        return ["area_type = building.disaggregate(zone.area_type_id, intermediates=[parcel])",
                "home_area_type  = household.disaggregate(building.area_type)",
                "is_home_area_type_%s = (person.disaggregate(household.home_area_type)==%s).astype(int32)" % (self.home_area_type, self.home_area_type),
                "is_workplace_area_type_%s = (job.disaggregate(building.area_type)==%s).astype(int32)" % (self.workplace_area_type, self.workplace_area_type),
            ]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply("is_home_area_type_%s" % self.home_area_type, 
                                           "is_workplace_area_type_%s" % self.workplace_area_type)

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
                 "area_type":   array([1,3,1,2])
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
        should_be = array([[0,0,1,0,1],
                           [0,0,1,0,1],
                           [0,0,1,0,1],
                           [0,0,1,0,1],
                           
                           [0,0,1,0,1],
                           [0,0,0,0,0],
                           [0,0,0,0,0],
                           [0,0,0,0,0],
                       ])
                            
        instance_name = 'psrc_parcel.person_x_job.home_area_type_1_workplace_area_type_2'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)



if __name__=='__main__':
    opus_unittest.main()