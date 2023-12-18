# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class hhfemale(Variable):
    """"""
        
    _return_type="bool8"

    def dependencies(self):
        return [my_attribute_label("sex")]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("sex") == 2


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "paris.household.hhfemale"

    def test_my_inputs(self):
        """
        """
        hh = array([2, 1, 2])

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"household":{ \
                "sex":hh}}, \
            dataset = "household")
        should_be = array([1, 0, 1])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-6), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()