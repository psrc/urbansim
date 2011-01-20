# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import zeros, where, float32, take, array

class ln_access_from_residence_to_workplaces_if_income_DDD(Variable):
    """For each household, the accessibilty from this household's residence to any workplace
    (if the household is of this income category), or zero otherwise.
    """
    _return_type="float32"
    def __init__(self, number):
        self.income_type = number
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("gridcell", 'ln_access_from_residence_to_workplaces_%d' % self.income_type),
                attribute_label("household", "is_income_%d" % self.income_type)
                ]

    def compute(self, dataset_pool):
        return_vals = zeros((self.get_dataset().get_reduced_n(),self.get_dataset().get_reduced_m()),
                            dtype=self._return_type)
        inc_DDD_idx = where(self.get_dataset().get_attribute_of_dataset("is_income_%d" % self.income_type))[0]
        trip2Darray = self.get_dataset().get_2d_dataset_attribute('ln_access_from_residence_to_workplaces_%d' % self.income_type)
        return_vals[inc_DDD_idx,:] = take(trip2Darray, inc_DDD_idx, axis=0).astype(self._return_type)
        return return_vals


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def get_values(self, income_type):
        return VariableTestToolbox().compute_variable(
                "urbansim.household_x_gridcell.ln_access_from_residence_to_workplaces_if_income_%d" % income_type,
            {"household":{
                "is_income_1": array([1,0,0,0]),
                "is_income_2": array([0,1,1,0]),
                "is_income_3": array([0,0,0,0]),
                "is_income_4": array([0,0,0,1])},
             "gridcell":{
                 "ln_access_from_residence_to_workplaces_1": array([1.1, 11.1, 111.1]),
                 "ln_access_from_residence_to_workplaces_2": array([2.2, 22.2, 222.2]),
                 "ln_access_from_residence_to_workplaces_3": array([3.3, 33.3, 333.3]),
                 "ln_access_from_residence_to_workplaces_4": array([4.4, 44.4, 444.4])}},
            dataset = "household_x_gridcell")

    def test_income_type_1(self):
        values = self.get_values(1)
        should_be = array([[1.1, 11.1, 111.1], # in gc 1, income type = 1
                           [0.0, 0.0, 0.0], # in gc 2, income type = 2
                           [0.0, 0.0, 0.0],  # in gc 2, income type = 2
                           [0.0, 0.0, 0.0]]) # in gc 1, income type = 3

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4),
                         True, msg = "Error in ln_access_from_residence_to_workplaces_if_income_1")

    def test_income_type_2(self):
        values = self.get_values(2)

        should_be = array([[0.0, 0.0, 0.0], # in gc 1, income type = 1
                           [2.2, 22.2, 222.2], # in gc 2, income type = 2
                           [2.2, 22.2, 222.2],  # in gc 2, income type = 2
                           [0.0, 0.0, 0.0]]) # in gc 1, income type = 3

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4),
                         True, msg = "Error in ln_access_from_residence_to_workplaces_if_income_2")

    def test_income_type_3(self):
        values = self.get_values(3)

        should_be = array([[0.0, 0.0, 0.0], # in gc 1, income type = 1
                           [0.0, 0.0, 0.0], # in gc 2, income type = 2
                           [0.0, 0.0, 0.0],  # in gc 2, income type = 2
                           [0.0, 0.0, 0.0]]) # in gc 1, income type = 3

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4),
                         True, msg = "Error in ln_access_from_residence_to_workplaces_if_income_3")


if __name__ == "__main__":
    opus_unittest.main()