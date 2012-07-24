# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable_for_non_interaction_dataset import abstract_travel_time_variable_for_non_interaction_dataset

class travel_time_from_home_to_work(abstract_travel_time_variable_for_non_interaction_dataset):
    """travel_time_from_home_to_work"""

    default_value = 0
    origin_zone_id = "residence_zone_id = person.disaggregate(mag_zone.household.zone_id)"
    destination_zone_id = "workplace_zone_id = mag_zone.person.wtaz"
    travel_data_attribute = "travel_data.peak_travel_time"

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
                'household_id':array([1, 1, 2, 3, 3, 5]),
                #hhzone_id    :array([3, 3, 1, 1, 1, 2]),
                'job_id':      array([1, 2, -1, -1, 2, 3]),
                #jobzone_id:   array([1, 2, -1, -1, 2, 3])
                }, 
             "job":{ 
                'job_id': array([1, 2, 3]),
                'zone_id':array([1, 2, 3]),
                },
             "household":{
                'household_id':array([1, 2, 3, 4, 5]),
                'zone_id':     array([3, 1, 1, 1, 2]),
                 },
            'travel_data':{
                'from_zone_id':              array([3,     3,   1,   1,   1,   2,   2,   3,   2]),
                'to_zone_id':                array([1,     3,   1,   3,   2,   1,   3,   2,   2]),
                'am_single_vehicle_to_work_travel_time':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
            },
         })
        should_be = array([1.1, 7.8, 0, 0, 0.5, 8.7])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
