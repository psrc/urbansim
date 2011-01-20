# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import reshape
from numpy import ma

class income_to_avg_val_per_unit_ratio(Variable):
    """ income / (avg_val_per_unit_residential/10)""" 
    
    _return_type="float32"
    
    val_per_unit = "avg_val_per_unit_residential"
    hh_income = "income"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.val_per_unit), \
                attribute_label("household", self.hh_income)]
        
    def compute(self,  arguments=None):
        ds = self.get_dataset()
        income = reshape(ds.get_attribute_of_dataset(self.hh_income),(ds.get_reduced_n(), 1))
        resval = (ds.get_2d_dataset_attribute(self.val_per_unit)/10.0)
        return income / ma.masked_where(resval == 0, resval)
                

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.income_to_avg_val_per_unit_ratio"
    def test_my_inputs(self):
        res_value = array([333.0, 500.55, 1000.26, 459, 0])
        income = array([1, 20, 500])

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"gridcell":{ \
                "avg_val_per_unit_residential": res_value}, \
            "household":{ \
                "income":income}}, \
            dataset = "household_x_gridcell")
        should_be = array([[1.0/33.30, 1.0/50.055, 1.0/100.026, 1.0/45.90, 0], 
                           [20.0/33.3, 20.0/50.055, 20.0/100.026, 20.0/45.9, 0], 
                           [500.0/33.3,  500.0/50.055,  500.0/100.026,  500.0/45.9, 0]])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-5), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()