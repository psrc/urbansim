# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.simulation_state import SimulationState
from numpy import maximum, ma, logical_not

class age_masked(Variable):
    """The age of the building, computed by subtracting the year built
    from the current simulation year. Entries that have invalid year_built are masked."""

    year_built = "year_built"
    _return_type="float32"  #TODO: this is a work around for numpy ndimage would not working with int

    def dependencies(self):
        return [my_attribute_label(self.year_built), my_attribute_label("has_valid_year_built")]

    def compute(self, dataset_pool):
        current_year = SimulationState().get_current_time()

        if current_year == None:
            raise StandardError, "'SimulationState().get_current_time()' returns None."
        is_year_built = self.get_dataset().get_attribute("has_valid_year_built")
        building_age = maximum(0, current_year - self.get_dataset().get_attribute(self.year_built))
        return ma.masked_where( logical_not(is_year_built), building_age)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


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
                    'year_built': array([1995, 2000, 2006, 200])
                    },
                'urbansim_constant':{
                    'absolute_min_year': array([1800])
                }
            }
        )

        SimulationState().set_current_time(2005)
        should_be = array([10, 5, 0, -999])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()