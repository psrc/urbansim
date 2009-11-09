# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, where, float32, put, take
#from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class trip_weighted_average_utility_hbw_to_work_am_income_if_income_DDD(Variable):
    """For each household, the trip_weighted_average_utility_hbw_to_work for this household's
    residence (if this household is of this income category), or zero otherwise.
    """
    _return_type="float32"
    def __init__(self, number):
        self.income_type = number
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("gridcell", "trip_weighted_average_utility_hbw_to_work_am_income_%d" % self.income_type),
                attribute_label("household", "is_income_%d" % self.income_type)
                ]

    def compute(self, dataset_pool):
        return_vals = zeros((self.get_dataset().get_reduced_n(),self.get_dataset().get_reduced_m()),
                            dtype=self._return_type)

        inc_DDD_idx = where(self.get_dataset().get_attribute_of_dataset("is_income_%d" % self.income_type))[0]
        trip2Darray = self.get_dataset().get_2d_dataset_attribute('trip_weighted_average_utility_hbw_to_work_am_income_%d' % self.income_type)
        return_vals[inc_DDD_idx,:] = take(trip2Darray, inc_DDD_idx, axis=0).astype(self._return_type)
        return return_vals


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def get_values(self, income_type):
        return VariableTestToolbox().compute_variable(
                "urbansim.household_x_gridcell.trip_weighted_average_utility_hbw_to_work_am_income_if_income_%d" % income_type,
            {"household":{
                "grid_id":array([1,1,2,2]),
                "is_income_1": array([1, 0, 0, 0]),
                "is_income_2": array([0, 0, 0, 0]),
                "is_income_3": array([0, 1, 1, 0]),
                "is_income_4": array([0, 0, 0, 1]) },
             "gridcell":{
                "trip_weighted_average_utility_hbw_to_work_am_income_1": array([10.4, 20.5]),
                "trip_weighted_average_utility_hbw_to_work_am_income_2": array([20.4, 13.8]),
                "trip_weighted_average_utility_hbw_to_work_am_income_3": array([30.4, 10.0]),
                "trip_weighted_average_utility_hbw_to_work_am_income_4": array([40.4, 50.7])
                 } },
            dataset = "household_x_gridcell")

    def test_income_type_1(self):
        values = self.get_values(1)
        should_be = array([[10.4, 20.5], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
        self.assertEqual(ma.allclose(values, should_be),
                         True, msg = "Error in trip_weighted_average_utility_hbw_to_work_am_income_1")

    def test_income_type_2(self):
        values = self.get_values(2)
        should_be = array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])

        self.assertEqual(ma.allclose(values, should_be),
                         True, msg = "Error in trip_weighted_average_utility_hbw_to_work_am_income_2")

    def test_income_type_3(self):
        values = self.get_values(3)
        should_be = array([[0.0, 0.0], [30.4, 10.0], [30.4, 10.0], [0.0, 0.0]])

        self.assertEqual(ma.allclose(values, should_be),
                         True, msg = "Error in trip_weighted_average_utility_hbw_to_work_am_income_3")

    def test_income_type_4(self):
        values = self.get_values(4)
        should_be = array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [40.4, 50.7]])

        self.assertEqual(ma.allclose(values, should_be),
                         True, msg = "Error in trip_weighted_average_utility_hbw_to_work_am_income_4")


if __name__=='__main__':
    opus_unittest.main()