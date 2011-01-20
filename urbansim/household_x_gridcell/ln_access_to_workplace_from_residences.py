# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import ones, array, float32

class ln_access_to_workplace_from_residences(Variable):
    """(SUM(Jobs(i) * exp(logsum_DDD(i to this_zone)), for i=zone_1...zone_n), for
        the income type (DDD) of this house) / number_of_DDD_types

        Although, the above fomula is really calculated in zones and passed through gridcell
        to household.
    """
    gc_ln_access_to_workplace_from_residences = "gc_ln_access_to_workplace_from_residences"
    hh_grid_id = "grid_id"

    def dependencies(self):
        return [attribute_label("gridcell", self.gc_ln_access_to_workplace_from_residences),
                attribute_label("household", self.hh_grid_id)
                ]

    def compute(self, dataset_pool):
        return self.get_dataset().get_2d_dataset_attribute('gc_ln_access_to_workplace_from_residences')


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.ln_access_to_workplace_from_residences"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"household":{
                "grid_id": array([1, 2, 3, 1])},
             "gridcell":{
                 "gc_ln_access_to_workplace_from_residences": array([1.1, 11.1, 111.1])}},
            dataset = "household_x_gridcell")

        should_be = array([[1.1, 11.1, 111.1],
                           [1.1, 11.1, 111.1],
                           [1.1, 11.1, 111.1],
                           [1.1, 11.1, 111.1]])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4),
                         True, msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()