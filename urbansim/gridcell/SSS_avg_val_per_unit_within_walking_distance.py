# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class SSS_avg_val_per_unit_within_walking_distance(Variable):
    """Average value per unit of given type within walking distance, computed by dividing the 
    total value within walking distance by the number of units (res units/industrial/commercial sqft) within walking distance """

    def __init__(self, type):
        self.value_within_walking_distance = "value_of_%s_space_within_walking_distance" % type
        self.units_within_walking_distance = "total_buildings_%s_space_where_tv_within_walking_distance" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.value_within_walking_distance), 
                my_attribute_label(self.units_within_walking_distance)]

    def compute(self, dataset_pool):
        return self.safely_divide_two_attributes(self.value_within_walking_distance, 
                                               self.units_within_walking_distance, -1.0)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", ma.filled(values,0.0))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        value_within_walking_distance = array([1000, 5000, 10000, 15000])
        units_within_walking_distance = array([0.0, 100.0, 300.0, 56.0])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id": array([1,2,3,4]),
                    "value_of_residential_space_within_walking_distance": value_within_walking_distance, 
                    "total_buildings_residential_space_where_tv_within_walking_distance": units_within_walking_distance
                } 
            }
        )
        instance_name = "urbansim.gridcell.residential_avg_val_per_unit_within_walking_distance"
        should_be = array([-1.0, 50.0, 33.3333333, 267.8571429])
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
