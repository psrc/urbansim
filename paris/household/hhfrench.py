# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class hhfrench(Variable):
    """"""
        
    _return_type="bool8"

    def dependencies(self):
        return [my_attribute_label("foreign_born")]

    def compute(self, dataset_pool):
        return 1 - self.get_dataset().get_attribute("foreign_born")


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "paris.household.hhfrench"

    def test_my_inputs(self):
        """
        """
        hh = array([1, 0, 1])

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"household":{ \
                "foreign_born":hh}}, \
            dataset = "household")
        should_be = array([0, 1, 0])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-6), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()