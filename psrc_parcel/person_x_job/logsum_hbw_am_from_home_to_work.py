#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from psrc.variables.abstract_travel_time_variable import abstract_travel_time_variable
from opus_core.misc import unique_values
from numpy import where, repeat, ones, float32, resize, array
from numpy import ma
from opus_core.logger import logger

class logsum_hbw_am_from_home_to_work(abstract_travel_time_variable):
    """logsum_hbw_am_from_home_to_work
       logsum breaks by income:
           Less than $25K;
           $25K to $45K;
           $45 to $75K;
           More than $75K.
    """
    default_value = -1
    agent_zone_id = "zone_id = person.disaggregate(urbansim_parcel.household.zone_id)"
    location_zone_id = "urbansim_parcel.job.zone_id"
    direction_from_home = True
    
    def dependencies(self):
        return [ self.agent_zone_id, self.location_zone_id,
                 "income_breaks = 1 * (household.income < 25000) +" + \
                                " 2 * numpy.logical_and(household.income >= 25000, household.income < 45000) +" + \
                                " 3 * numpy.logical_and(household.income >= 45000, household.income < 75000) +" + \
                                " 4 * (household.income >= 75000)",
                 "income_breaks = ( person.disaggregate(household.income_breaks) ).astype(int32)"]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        income_breaks = interaction_dataset.get_dataset(1).get_attribute_by_index("income_breaks",
                                                                               interaction_dataset.get_2d_index_of_dataset1())
        unique_income_breaks = unique_values(income_breaks.ravel())
        self.add_dependencies(["travel_data.logsum_hbw_am_income_" + str(i) for i in unique_income_breaks])
        
        travel_data = dataset_pool.get_dataset('travel_data')
        var1 = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_zone_id,
                                                                         interaction_dataset.get_2d_index_of_dataset1())
        var2 = interaction_dataset.get_2d_dataset_attribute(self.location_zone_id)
        if self.direction_from_home:
            home_zone = var1
            work_zone = var2
        else:
            home_zone = var2
            work_zone = var1
        times = resize(array([self.default_value], dtype=float32), home_zone.shape)
        positions = ones(home_zone.shape, dtype="int32")
        #create indices for 2d array of (origin, destination)
        ij = map(lambda x, y: (x, y), where(positions)[0], where(positions)[1])
        for a in ij:
            i, j = a
            try:
                times[i,j] = travel_data.get_attribute_by_id("logsum_hbw_am_income_" + str(income_breaks[i, j]) , (home_zone[i,j], work_zone[i,j]))
            except:
                logger.log_warning("zone pairs (%s, %s) is not in zoneset; value set to %s." % (home_zone[i,j], work_zone[i,j], self.default_value))

        return times
    

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
