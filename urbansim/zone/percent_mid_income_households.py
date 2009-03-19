# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 
from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
from variable_functions import my_attribute_label

class percent_mid_income_households(Variable):
    """The number_of_mid_income_households / number_of_households. """

    _return_type="float32"
    mid_income = "number_of_mid_income_households"
    number_of_households = "number_of_households"
    
    def dependencies(self):
        return [my_attribute_label(self.number_of_households), 
                my_attribute_label(self.mid_income)]
        
    def compute(self, dataset_pool):
        return 100*safe_array_divide(self.get_dataset().get_attribute(self.mid_income),
                               self.get_dataset().get_attribute(self.number_of_households))
 


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.percent_mid_income_households"

    def test_my_inputs(self):
        mid_income_hhs = array([8, 0, 35, 0])
        number_of_households = array([10, 20, 35, 0])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "number_of_mid_income_households":mid_income_hhs, 
                "number_of_households":number_of_households}}, 
            dataset = "zone")
        should_be = array([800.0/10.0, 0, 100, 0])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()