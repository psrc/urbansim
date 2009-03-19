# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from psrc.abstract_variables.abstract_logsum_variable import abstract_logsum_variable
from opus_core.misc import unique_values
from numpy import where, repeat, ones, float32, resize, array
from numpy import ma
from opus_core.logger import logger

class logsum_hbw_am_from_home_to_work(abstract_logsum_variable):
    """logsum_hbw_am_from_home_to_work
       logsum breaks by income:
           Less than $25K;
           $25K to $45K;
           $45 to $75K;
           More than $75K.
    """
    
    default_value = -9
    agent_zone_id = "zone_id = person.disaggregate(urbansim_parcel.household.zone_id)"
    agent_category_attribute = "logsum_income_break =( person.disaggregate(psrc.household.logsum_income_break)).astype(int32)"
    location_zone_id = "urbansim_parcel.job.zone_id"
    travel_data_attributes = {1: "travel_data.logsum_hbw_am_income_1", 
                              2: "travel_data.logsum_hbw_am_income_2", 
                              3: "travel_data.logsum_hbw_am_income_3", 
                              4: "travel_data.logsum_hbw_am_income_4" }
    direction_from_home = True

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import arange, array
from numpy import ma
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
              #homezone_id:           3, 3, 2, 1, 1, 1
              #income_brk:            4, 4, 2, 1, 1, 1
                }, 
             "job":{ 
                 'job_id': array([1, 2, 3]),
                 'zone_id':array([1, 2, 3]),
                },
             "household":{
                 'household_id':array([1, 2, 3, 4, 5]),
                 'zone_id':     array([3, 1, 1, 1, 2]),
                 'income':      array([8, 5, 2, 0, 3]) * 10000
                 },
             "travel_data":{
                 'from_zone_id':          array([3,     3,   1,   1,   1,   2,   2,   3,   2]),
                 'to_zone_id':            array([1,     3,   1,   3,   2,   1,   3,   2,   2]),
                 'logsum_hbw_am_income_1':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0]),
                 'logsum_hbw_am_income_2':array([0.9, 2.0, 3.1, 4.2, 0.3, 0.5, 8.5, 7.6, 0.8]),
                 'logsum_hbw_am_income_3':array([0.7, 1.8, 2.9, 4.0, 0.1, 0.3, 8.3, 7.4, 0.6]),
                 'logsum_hbw_am_income_4':array([0.5, 1.6, 2.7, 3.8,-0.1, 0.1, 8.1, 7.2, 0.4])                 
             }
         })
        should_be = array([[0.5, 7.2, 1.6], 
                           [0.5, 7.2, 1.6],
                           [0.5, 0.8, 8.5],
                           [3.3, 0.5, 4.4],
                           [3.3, 0.5, 4.4],
                           [3.3, 0.5, 4.4]])
                            
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
