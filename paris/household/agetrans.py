# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class agetrans(Variable):
    """"""
        
    _return_type="float32"

    def dependencies(self):
        return [my_attribute_label("age")]

    def compute(self, dataset_pool):
        age = self.get_dataset().get_attribute("age")
        agetrans = (age-20)/10.0
        return agetrans


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "paris.household.agetrans"

    def test_my_inputs(self):
        """
        """
        hh = array([21, 75, 6])

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"household":{ \
                "age":hh}}, \
            dataset = "household")
        should_be = array([0.1, 5.5, -1.4])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-6), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()