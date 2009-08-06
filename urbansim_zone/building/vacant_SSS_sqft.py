# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import clip_to_zero_if_needed

class vacant_SSS_sqft(Variable):
    """ The total_SSS_sqft - occupied_building_sqft. """ 

    _return_type = "int32"
    
    def __init__(self, type):
        self.occupied_sqft = "occupied_building_sqft_by_%s_jobs" % type
        self.total_sqft = "total_%s_sqft" % type
        self.variable_name = "vacant_%s_sqft" % type
        Variable.__init__(self)

    def dependencies(self):
        return ["urbansim_zone.building.%s" % self.occupied_sqft, 
                "urbansim_zone.building.%s" % self.total_sqft]                             

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return  clip_to_zero_if_needed(ds.get_attribute(self.total_sqft) - 
                    ds.get_attribute(self.occupied_sqft), self.variable_name)
    


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone', 'urbansim'],
            test_data={
             'building':
                 {"building_id":         array([1,  2, 3, 4,  5]),
                  "building_type_id":    array([1,  2, 1, 1,  2]),
                  "zone_id":             array([1,  1, 3, 2,  2]),
                  "non_residential_sqft": array([2000, 3, 10, 35, 200]),
                  "number_of_commercial_jobs": array([12, 0, 20, 5, 0]),
                  "building_sqft_per_job": array([10, 20, 30, 5, 0])
                },
            'building_type':
            {
             "building_type_id":array([1,2]),
             "name":array(["commercial", "industrial"])
             },
            }
        )
    
        should_be = array([2000-12*10, 0, 0, 35-5*5, 0])
        instance_name = "urbansim_zone.building.vacant_commercial_sqft"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()