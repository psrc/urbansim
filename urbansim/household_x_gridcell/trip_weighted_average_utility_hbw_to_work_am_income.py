# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, where, float32, put, take
#from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class trip_weighted_average_utility_hbw_to_work_am_income(Variable):
    """What is the trip_weighted_average_utility_hbw_to_work for this household. """
    _return_type="float32"
    # todo: how to not hard code the income values?
    gc_wauh_to_work_ai_1 = "trip_weighted_average_utility_hbw_to_work_am_income_1"
    gc_wauh_to_work_ai_2 = "trip_weighted_average_utility_hbw_to_work_am_income_2"
    gc_wauh_to_work_ai_3 = "trip_weighted_average_utility_hbw_to_work_am_income_3"
    gc_wauh_to_work_ai_4 = "trip_weighted_average_utility_hbw_to_work_am_income_4"
    hh_income_1 = "is_income_1"
    hh_income_2 = "is_income_2"
    hh_income_3 = "is_income_3"
    hh_income_4 = "is_income_4"

    def dependencies(self):
        return [attribute_label("gridcell", self.gc_wauh_to_work_ai_1),
                attribute_label("gridcell", self.gc_wauh_to_work_ai_2),
                attribute_label("gridcell", self.gc_wauh_to_work_ai_3),
                attribute_label("gridcell", self.gc_wauh_to_work_ai_4),
                attribute_label("household", self.hh_income_1),
                attribute_label("household", self.hh_income_2),
                attribute_label("household", self.hh_income_3),
                attribute_label("household", self.hh_income_4)
                ]

    def compute(self, dataset_pool):
        return_vals = zeros((self.get_dataset().get_reduced_n(),self.get_dataset().get_reduced_m()),
                            dtype=self._return_type)

        for income_type in range(1, 5):
            inc_DDD_idx = where(self.get_dataset().get_attribute_of_dataset("is_income_%d" % income_type))[0]
            trip2Darray = self.get_dataset().get_2d_dataset_attribute('trip_weighted_average_utility_hbw_to_work_am_income_%d' % income_type)
            return_vals[inc_DDD_idx,:] = take(trip2Darray, inc_DDD_idx, axis=0).astype(self._return_type)
        return return_vals


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.trip_weighted_average_utility_hbw_to_work_am_income"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name,
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
        should_be = array([[10.4, 20.5], [30.4, 10.0], [30.4, 10.0], [40.4, 50.7]])

        self.assertEqual(ma.allclose(values, should_be),
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()