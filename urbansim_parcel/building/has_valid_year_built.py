# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.simulation_state import SimulationState
from numpy import maximum, ma

class has_valid_year_built(Variable):
    """If buildings have valid year_built or not."""

    year_built = "year_built"

    def dependencies(self):
        return [my_attribute_label(self.year_built)]

    def compute(self, dataset_pool):
        urbansim_constant = dataset_pool.get_dataset('urbansim_constant')
        return self.get_dataset().get_attribute(self.year_built) >= urbansim_constant["absolute_min_year"]

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
                'building':{
                    'building_id': array([1,2,3,4]),
                    'year_built': array([1995, 1800, 2006, 200])
                    },
                'urbansim_constant':{
                    'absolute_min_year': array([1800])
                }
            }
        )

        SimulationState().set_current_time(2005)
        should_be = array([True, True, True, False])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()