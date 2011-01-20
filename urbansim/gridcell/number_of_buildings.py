# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class number_of_buildings(Variable):
    """The total number of buildings in the cell."""

    number_of_buildings = "gridcell.number_of_agents(building)"
        
    def dependencies(self):
        return [self.number_of_buildings]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.number_of_buildings)
                      


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell": { 
                    "grid_id": array([1, 2, 3])
                    },
                "building": {
                    "building_id": array([1, 2, 3, 4, 5, 6, 7]),
                    "grid_id":     array([1, 1, 2, 3, 1, 2, 1]),
                }
            }
        )

        should_be = array([4, 2, 1]) 
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()