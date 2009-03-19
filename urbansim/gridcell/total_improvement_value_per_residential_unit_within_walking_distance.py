# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class total_improvement_value_per_residential_unit_within_walking_distance(Variable):

    total_improvement_value_within_walking_distance = "total_improvement_value_within_walking_distance"
    residential_units_within_walking_distance = "residential_units_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.total_improvement_value_within_walking_distance),
                my_attribute_label(self.residential_units_within_walking_distance)]

    def compute(self, dataset_pool):
        units_wwd = self.get_dataset().get_attribute(self.residential_units_within_walking_distance)
        return self.get_dataset().get_attribute(self.total_improvement_value_within_walking_distance) /\
               ma.masked_where(units_wwd == 0, units_wwd.astype(float32))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'total_residential_value': array([100, 500, 1000, 1500]),
                    'governmental_improvement_value': array([100, 500, 1000, 1500]),
                    # The four items below are 'throw-away' items to allow this Variable to test -
                    # they can be anything and not affect the outcome of this variable.
                    'commercial_improvement_value': array([0, 0, 0, 0]),
                    'industrial_improvement_value': array([0, 0, 0, 0]),
                    'residential_improvement_value': array([0, 0, 0, 0]),
                    'residential_units': array([0, 0, 0, 0]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        should_be = array([1800, 3100, 4600, 6000])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()