# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable
class workerDDD_drive_alone_hbw_am_travel_time_from_home_to_work(abstract_travel_time_variable):
    """drive_alone_hbw_am_travel_time_from_home_to_work"""

    default_value = 180
    
    def __init__(self, number):
        self.agent_zone_id = "work%s_workplace_zone_id = household.aggregate((person.worker%s == 1) * urbansim_parcel.person.workplace_zone_id).astype(int32)" % (number, number)
        self.location_zone_id = "urbansim_parcel.building.zone_id"
        self.travel_data_attribute = "urbansim.travel_data.am_single_vehicle_to_work_travel_time"
        self.direction_from_home = False
        abstract_travel_time_variable.__init__(self)

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import ma, array
class Tests(opus_unittest.OpusTestCase):
        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            'person': {
                'person_id':array([1, 2, 3, 4, 5, 6]),
                'household_id':array([1, 1, 2, 3, 3, 3]),
                'member_id':array([1, 2, 1, 1, 2, 3]),
                'worker1':array([1, 0, 1, 0, 0, 1]),
                'workplace_zone_id':array([1, 3, 3, 2, 1, 3]),
                },
            'building': {
                'building_id':array([1,2,3,4]),
                'zone_id':array([1, 1, 3, 2])
                },
            'household': {
                'household_id':array([1,2,3,4,5]),
                'zone_id':array([3, 1, 1, 1, 2]),
            },
            'travel_data': {
                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
                'am_single_vehicle_to_work_travel_time':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
            }
        }
        )
        default_value = workerDDD_drive_alone_hbw_am_travel_time_from_home_to_work.default_value
        should_be = array([[3.3, 3.3, 1.1, 0.7],
                           [4.4, 4.4, 2.2, 8.7],
                           [4.4, 4.4, 2.2, 8.7],
                           [default_value, default_value, default_value, default_value],
                           [default_value, default_value, default_value, default_value]])

        instance_name = "psrc_parcel.household_x_building.worker1_drive_alone_hbw_am_travel_time_from_home_to_work"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
    