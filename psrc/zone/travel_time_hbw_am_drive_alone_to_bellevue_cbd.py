# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, where, minimum
from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class travel_time_hbw_am_drive_alone_to_bellevue_cbd(Variable):
    """Travel time to the Bellevue CBD. It is the minimum of travel times to zones that have bellevue_cbd=1.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    _return_type = 'float32'
    
    def dependencies(self):
        return ['zone.bellevue_cbd']

    def compute(self, dataset_pool):
        zones = self.get_dataset()
        is_in_cbd = zones.get_attribute('bellevue_cbd')
        zones_in_cbd = zones.get_id_attribute()[where(is_in_cbd)]
        min_values = array(zones.size()*[2**30], dtype=self._return_type)
        for zone_id in zones_in_cbd:
            variable_name = my_attribute_label("travel_time_hbw_am_drive_alone_to_%s" % zone_id)
            self.add_and_solve_dependencies([variable_name], dataset_pool=dataset_pool)
            min_values = minimum(min_values, zones.get_attribute(variable_name))
            
        min_within_cbd = min_values[where(is_in_cbd)].min()
        min_values[where(is_in_cbd)] = min_within_cbd
        return min_values
    

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
        __file__,
        package_order=['parcel','urbansim'],
        test_data={
            'zone': {
                "zone_id":array([1,3,4,7,15]),
                "travel_time_hbw_am_drive_alone_to_3": array([2, 1, 5, 20, 10]),
                "travel_time_hbw_am_drive_alone_to_15": array([1, 6, 10, 3, 0]),
                "bellevue_cbd": array([0, 1, 0, 0, 1])
            }
            }
        )
        should_be = array([1,0,5,3,0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()