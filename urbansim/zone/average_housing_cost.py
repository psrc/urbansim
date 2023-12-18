# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class average_housing_cost(Variable):
    """The total_housing_cost / residential_units. """

    total_housing_cost = "total_housing_cost"
    residential_units = "residential_units"
    
    def dependencies(self):
        return [my_attribute_label(self.total_housing_cost), 
                my_attribute_label(self.residential_units)]
        
    def compute(self, dataset_pool):
        units = self.get_dataset().get_attribute(self.residential_units)
        return ma.filled(self.get_dataset().get_attribute(self.total_housing_cost) / 
                ma.masked_where(units == 0, units.astype(float32)),0)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.average_housing_cost"

    def test_my_inputs(self):
        total_hcost = array([1000, 5000, 10000, 3000, 0])
        residential_units = array([1, 2, 3, 0, 2])
            
        values = VariableTestToolbox().compute_variable(self.variable_name, 
                {"zone":{ 
                "total_housing_cost":total_hcost, 
                "residential_units":residential_units}}, 
            dataset = "zone")
        should_be = array([1000.0, 2500.0, 3333.333, 0, 0])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-6), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()