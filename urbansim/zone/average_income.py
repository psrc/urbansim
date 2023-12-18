# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.gridcell.average_income import average_income as gc_average_income

class average_income(Variable):
    """The sum_income / number_of_households. """

    sum_income = "sum_income"
    number_of_households = "number_of_households"
    
    def dependencies(self):
        return [my_attribute_label(self.number_of_households), 
                my_attribute_label(self.sum_income)]
        
    def compute(self, dataset_pool):
        income_class = gc_average_income()
        income_class.set_dataset(self.get_dataset())
        return income_class.compute(dataset_pool)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.average_income"

    def test_my_inputs(self):
        sum_income = array([1000.0, 5000.0, 10000.0])
        number_of_households = array([1, 2, 3])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "sum_income":sum_income, 
                "number_of_households":number_of_households}}, 
            dataset = "zone")
        should_be = array([1000.0, 2500.0, 3333.333])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()