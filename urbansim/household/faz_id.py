# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class faz_id(Variable):
    """The Forecast Analysis Zone id of this household. """

    gc_faz_id = "faz_id"

    def dependencies(self):
        return [my_attribute_label("grid_id"), attribute_label("gridcell", self.gc_faz_id)]

    def compute(self, dataset_pool):
        return self.get_dataset().compute_variables(["household.disaggregate(gridcell.%s)" % self.gc_faz_id],
                                                    dataset_pool=dataset_pool)

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.faz_id"

    def test_my_inputs(self):
        grid_id = array([2, 1, 3])
        faz_id = array([4, 5, 6])

        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"household":{
                "grid_id":grid_id},
             "gridcell":{
                 "grid_id": array([1,2,3], dtype="int32"),
                  "faz_id": faz_id
                } },
            dataset = "household")
        should_be = array([5,4,6])

        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()