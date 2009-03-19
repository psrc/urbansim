# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_buildings_with_year_built(Variable):
    """Returns 1 if the location contains at least one buildings with valid year_built, otherwise 0.
        The variable average_building_age returns -1 for cells that do not contain such buildings.
    """

    _return_type="bool8"

    age = "average_building_age"
        
    def dependencies(self):
        return [my_attribute_label(self.age)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.age) >= 0


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from opus_core.simulation_state import SimulationState

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        SimulationState().set_current_time(2005)
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell": { 
                    "grid_id": array([1,2,3])
                    },
                "building": {
                    "building_id": array([1,2,3,4,5,6,7]),
                    "grid_id":     array([1,    1,     2,  3, 1,  2,  1]),
                    "year_built":  array([1995, 2000, 2005, 0, 10, 0, 2005])
                    },
                'urbansim_constant':{
                    "absolute_min_year": array([1800]),
                }
            }
        )

        should_be = array([True, True, False]) 
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()