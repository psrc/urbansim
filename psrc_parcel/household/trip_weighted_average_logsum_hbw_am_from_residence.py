# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import unique_values
from numpy import zeros, float32, array
from numpy import ma
from opus_core.logger import logger

class trip_weighted_average_logsum_hbw_am_from_residence(Variable):
    """trip weighted logsum_hbw_am from a household's residence zone
    refer to psrc.zone.trip_weigthed_average_logsum_hbw_am_income_DDD
    
       logsum breaks by income:
           Less than $25K;
           $25K to $45K;
           $45 to $75K;
           More than $75K.
    """
    default_value = -99
    
    def dependencies(self):
        return [ "urbansim_parcel.household.zone_id",
                 "psrc.household.logsum_income_break",
             ]

    def compute(self, dataset_pool):
        hhs = self.get_dataset()
        zones = dataset_pool.get_dataset('zone')
        zone_id = hhs.get_attribute("zone_id")
        income_break = hhs.get_attribute("logsum_income_break")
        unique_income_breaks = unique_values(income_break)
        self.add_and_solve_dependencies(
            ["psrc.zone.trip_weighted_average_logsum_hbw_am_income_" + str(i) for i in unique_income_breaks],
            dataset_pool=dataset_pool
        )
        
        hhs_size = hhs.size()
        results = zeros(hhs_size, dtype="float32") + self.default_value
        for h in range(hhs_size):
            try:
                results[h] = zones.get_attribute_by_id("trip_weighted_average_logsum_hbw_am_income_" + str(income_break[h]), zone_id[h])
            except:
                logger.log_warning("zone_id %s for household %s is not in zoneset; value set to %s." % \
                                   (zone_id[h], hhs.get_id_attribute()[h], self.default_value))

        return results
    

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
             "household":{
                 'household_id':array([1, 2, 3, 4, 5]),
                 'zone_id':     array([3, 1,-1, 1, 2]),
                 'income':      array([8, 5, 2, 0, 3]) * 10000
                ##income_break: array([4, 3, 1, 1, 2])
                 },
             "zone":{
                 'zone_id':     array([1, 2, 3]),
                 },
             "travel_data":{
                 'from_zone_id':          array([ 3,     3,   1,   1,   1,   2,   2,   3,   2]),
                 'to_zone_id':            array([ 1,     3,   1,   3,   2,   1,   3,   2,   2]),
                 'logsum_hbw_am_income_1':array([ 1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0]),
                 'logsum_hbw_am_income_2':array([ 0.9, 2.0, 3.1, 4.2, 0.3, 0.5, 8.5, 7.6, 0.8]),
                 'logsum_hbw_am_income_3':array([ 0.7, 1.8, 2.9, 4.0, 0.1, 0.3, 8.3, 7.4, 0.6]),
                 'logsum_hbw_am_income_4':array([ 0.5, 1.6, 2.7, 3.8,-0.1, 0.1, 8.1, 7.2, 0.4]),
                 'am_pk_period_drive_alone_vehicle_trips':\
                                          array([11.0, 2.0,30.0, 4.0, 0.0, 1.0, 5.0, 2.0, 7.0]),
             }
         })
        should_be = array([(0.5*11.0 + 7.2*2.0 + 1.6*2.0) / (11.0 + 2.0 + 2.0),
                           (2.9*30.0 + 0.1*0.0 + 4.0*4.0) / (30.0 + 0.0 + 4.0),
                           trip_weighted_average_logsum_hbw_am_from_residence.default_value,
                           (3.3*30.0 + 0.5*0.0 + 4.4*4.0) / (30.0 + 0.0 + 4.0),
                           (0.5* 1.0 + 0.8*7.0 + 8.5*5.0)  / (1.0 + 7.0 + 5.0)])
                            
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
