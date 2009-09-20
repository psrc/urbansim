# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_time_space_prism_variable import abstract_time_space_prism_variable

class workerDDD_employment_of_group_retail_accessible_from_work_to_home_drive_alone(abstract_time_space_prism_variable):
    """"""

    default_value = 0
    _return_type="int32"

    def __init__(self, worker):
        self.agent_resource = "household.aggregate((person.worker%s==1).astype(int32)*(person.disaggregate(tour.arr_time - tour.dep_time - 15)))" % worker
        self.agent_zone_id = "worker%s_workplace_zone_id = household.aggregate((person.worker%s == 1).astype(int32) * urbansim_parcel.person.workplace_zone_id )" % (worker, worker)
        self.choice_zone_id = 'urbansim_parcel.building.zone_id'
        self.travel_data_attribute = 'travel_data.am_single_vehicle_to_work_travel_time'
        self.travel_data_attribute_default_value = 999
        self.zone_attribute_to_access = "urbansim_parcel.zone.number_of_jobs_of_sector_group_retail"
        self.direction_from_agent_to_choice = True
        
        abstract_time_space_prism_variable.__init__(self)
    
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import ma, array
class Tests(opus_unittest.OpusTestCase):
        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            "person":{ 
                'person_id':   array([1, 2, 3, 4, 5, 6]),
                'household_id':array([1, 1, 5, 3, 3, 3]),
                'member_id':   array([1, 2, 1, 1, 2, 3]),
                'worker1':     array([1, 0, 0, 1, 1, 1]),
                'tour_id':     array([1, 2, 1, 3, 2, 1])
                }, 
             "tour":{
                'tour_id':      array([1, 2, 3]),
                'arr_time':     array([100, 1000, 30]),
                'dep_time':     array([70,  940,  10]),
                     },
             "household":{
                 'household_id':array([1,2,3,4,5,6]),
                 'worker1_workplace_zone_id':array([1, 3, 3, 2, 3, -1]),
#                 'available_travel_time':array([6, 4.4, 4.3, 2, 17, 0])
                # agent_resourc
                 },
             "building":{
                 'building_id':array([1, 2, 3, 4]),
                 'parcel_id':  array([1, 1, 3, 4]),
                #'zone_id':    array([1, 1, 3, 2])
                 },             
             "parcel":{
                 'parcel_id':array([1, 2, 3, 4]),
                 'zone_id':  array([1, 1, 3, 2]),
                 },
             "zone":{
                 'zone_id':array([1, 2, 3]),
                 'number_of_jobs_of_sector_group_retail':array([7, 0, 103]),
                 },
             "travel_data":{
                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
                'am_single_vehicle_to_work_travel_time':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
                 },

         })
        
        should_be = array([[110, 110,   110,   110], 
                           [0, 0, 0,   0],
                           [110, 110, 110, 110], 
                           [0, 0,   0,   0],
                           [  0,   0,   0,   0],
                           [  0,   0,   0,   0], 
                           ])
        instance_name = 'psrc_parcel.household_x_building.worker1_employment_of_group_retail_accessible_from_work_to_home_drive_alone'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
#        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    
