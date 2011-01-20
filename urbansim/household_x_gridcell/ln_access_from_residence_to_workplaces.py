# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import zeros, where, float32, take, array

class ln_access_from_residence_to_workplaces(Variable):
    """Accessibilty from this residence to any workplace.
    """
    # TODO: how to not hard code the income values?
    _return_type="float32"
    gc_tfhtj_income_1 = "ln_access_from_residence_to_workplaces_1"
    gc_tfhtj_income_2 = "ln_access_from_residence_to_workplaces_2"
    gc_tfhtj_income_3 = "ln_access_from_residence_to_workplaces_3"
    gc_tfhtj_income_4 = "ln_access_from_residence_to_workplaces_4"
    hh_income_1 = "is_income_1"
    hh_income_2 = "is_income_2"
    hh_income_3 = "is_income_3"
    hh_income_4 = "is_income_4"

    def dependencies(self):
        return [attribute_label("gridcell", self.gc_tfhtj_income_1),
                attribute_label("gridcell", self.gc_tfhtj_income_2),
                attribute_label("gridcell", self.gc_tfhtj_income_3),
                attribute_label("gridcell", self.gc_tfhtj_income_4),
                attribute_label("gridcell", 'grid_id'),
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
            trip2Darray = self.get_dataset().get_2d_dataset_attribute('ln_access_from_residence_to_workplaces_%d' % income_type)
            return_vals[inc_DDD_idx,:] = take(trip2Darray, inc_DDD_idx, axis=0).astype(self._return_type)

        return return_vals



from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.ln_access_from_residence_to_workplaces"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"household":{
                "grid_id": array([1, 2, 3, 1]),
                "is_income_1": array([1,1,0,0]),
                "is_income_2": array([0,0,0,0]),
                "is_income_3": array([0,0,0,1]),
                "is_income_4": array([0,0,1,0])},
             "gridcell":{
                 "ln_access_from_residence_to_workplaces_1": array([1.1, 11.1, 111.1]),
                 "ln_access_from_residence_to_workplaces_2": array([2.2, 22.2, 222.2]),
                 "ln_access_from_residence_to_workplaces_3": array([3.3, 33.3, 333.3]),
                 "ln_access_from_residence_to_workplaces_4": array([4.4, 44.4, 444.4])}},
            dataset = "household_x_gridcell")

        should_be = array([[1.1, 11.1, 111.1], # in gc 1, income type = 1
                           [1.1, 11.1, 111.1], # in gc 2, income type = 1
                           [4.4, 44.4, 444.4],  # in gc 2, income type = 4
                           [3.3, 33.3, 333.3]]) # in gc 1, income type = 3

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4),
                         True, msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()