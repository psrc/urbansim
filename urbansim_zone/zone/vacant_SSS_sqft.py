# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class vacant_SSS_sqft(Variable):
    """ vacant_SSS_sqft aggregated over buildings """ 

    _return_type = "int32"
    
    def __init__(self, type):
        self.variable_name = "vacant_%s_sqft" % type
        Variable.__init__(self)

    def dependencies(self):
        return ["urbansim_zone.building.%s" % self.variable_name]                             

    def compute(self, dataset_pool):
        buildings = dataset_pool.get_dataset('building')
        return self.get_dataset().sum_dataset_over_ids(buildings, attribute_name=self.variable_name)
    


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
                 {"building_id":  array([1,2,3,4,5]),
                  "building_type_id":    array([1,  2, 1, 1,  2]),
                  "zone_id":             array([1,  1, 3, 2,  2]),
                  "vacant_commercial_sqft": array([20, 0, 10, 35, 0])
                },
            'zone':
            {
             "zone_id":array([1,2,3]),
             },
            'building_type':
            {
             "building_type_id":array([1,2]),
             "name":array(["commercial", "industrial"])
             },
            }
        )
    
        should_be = array([20, 35, 10])
        instance_name = "urbansim_zone.zone.vacant_commercial_sqft"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()