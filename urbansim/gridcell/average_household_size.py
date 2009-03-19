# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class average_household_size(Variable):
    """Computed by dividing population in the given cell by
        the total number of housholds in the cell"""

    population = "population"
    number_of_households = "number_of_households"

    def dependencies(self):
        return [my_attribute_label(self.number_of_households),
                my_attribute_label(self.population)]

    def pre_check(self, dataset_pool):
        idx = self.get_dataset().get_attribute("number_of_households")==0
        values = self.get_dataset().get_attribute("population")[idx]
        self.do_check("x == 0", values)

    def compute(self, dataset_pool):
        nh = self.get_dataset().get_attribute(self.number_of_households)
        return ma.filled(self.get_dataset().get_attribute(self.population)/
                      ma.masked_where(nh == 0, nh.astype(float32)), 0.0)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        population = array([1000, 10000, 100000]) #specify population for each of three locations
        number_of_households = array([300, 20, 500]) #specify the total number of households for each of three locations

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3]),
                    'population': population,
                    'number_of_households': number_of_households
                }
            }
        )

        should_be = array([3.33333, 500.0, 200.0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-6)

    def test_for_err(self):
        population = array([1000, 10000, 100000])
        number_of_households = array([1, 20, 500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3]),
                    'population': population,
                    'number_of_households': number_of_households
                }
            }
        )

        should_be = array([1000.0, 500.0, 200.0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()