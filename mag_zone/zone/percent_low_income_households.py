# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
#from urbansim.zone.variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class percent_low_income_households(Variable):
    """The number_of_low_income_households / number_of_households. """

    _return_type="float32"
    low_income = "number_of_low_income_households"
    number_of_households = "number_of_households"
    
    def dependencies(self):
        return [attribute_label("zone", self.number_of_households, "mag_zone"), 
                attribute_label("zone", self.low_income, "mag_zone")]
        
    def compute(self, dataset_pool):
        return 100*safe_array_divide(self.get_dataset().get_attribute(self.low_income),
                               self.get_dataset().get_attribute(self.number_of_households))
 


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "mag_zone.zone.percent_low_income_households"

    def test_my_inputs(self):
        low_income_hhs = array([8, 0, 35, 0])
        number_of_households = array([10, 20, 35, 0])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "number_of_low_income_households":low_income_hhs, 
                "number_of_households":number_of_households}}, 
            dataset = "zone")
        should_be = array([800.0/10.0, 0, 100, 0])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()