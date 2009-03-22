# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, repeat, ones, float32, resize, array
from numpy import ma
from urbansim.functions import attribute_label
from opus_core.logger import logger

class travel_time_from_home_to_work_drive_alone_hbw_am(Variable):
    """drive_alone_hbw_am_travel_time_from_home_to_work"""

    def __init__(self):
        self.default_value = 0
        self.origin_zone_id = "workplace_zone_id = urbansim_parcel.person.workplace_zone_id"
        self.dest_zone_id = "residence_zone_id = person.disaggregate(urbansim_parcel.household.zone_id)"
        self.travel_data_attribute = "urbansim.travel_data.am_single_vehicle_to_work_travel_time"
        self.direction_from_home = False
        Variable.__init__(self)
        
    def dependencies(self):
        return [ self.origin_zone_id, self.dest_zone_id, self.travel_data_attribute]

    def compute(self, dataset_pool):
        persons = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        travel_data_attr_mat = travel_data.get_attribute_as_matrix(self.travel_data_attribute, 
                                                                   fill=self.default_value)
        
        var1 = persons.get_attribute(self.origin_zone_id)
        var2 = persons.get_attribute(self.dest_zone_id)
        if self.direction_from_home:
            home_zone = var1.astype("int32")
            work_zone = var2.astype("int32")
        else:
            home_zone = var2.astype("int32")
            work_zone = var1.astype("int32")

        results = resize(array([self.default_value], dtype=float32), home_zone.shape)
        results = travel_data_attr_mat[home_zone, work_zone]
        
        missing_pairs_index = travel_data.get_od_pair_index_not_in_dataset(home_zone, work_zone)
        if missing_pairs_index[0].size > 0:
            results[missing_pairs_index] = self.default_value
            logger.log_warning("zone pairs at index %s are not in travel data; value set to %s." % ( str(missing_pairs_index), self.default_value) )
        
        return results
    
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import ma
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
