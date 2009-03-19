# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_SSS_buildings_with_year_built(Variable):
    """Returns 1 if the location contains buildings of the given type that have valid year_built, otherwise 0."""

    _return_type="bool8"

    def __init__(self, type):
        self.age = "average_building_age_%s" % type
        Variable.__init__(self)
        
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
                "gridcell":{ 
                    "grid_id": array([1,2,3])
                    },
                "building":{
                    "building_id": array([1,2,3,4,5,6,7]),
                    "grid_id": array([1, 1, 2, 3, 1, 2, 1]),
                    "year_built": array([1995, 2000, 2005, 0, 10, 0, 2005]),
                    "is_building_type_commercial": array([0,1,0,0,0,1,1])
                    },
                'urbansim_constant':{
                    "absolute_min_year": array([1800]),
                }
            }
        )
        
        should_be = array([True, False, False]) 
        instance_name = "urbansim.gridcell.has_commercial_buildings_with_year_built"     
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()