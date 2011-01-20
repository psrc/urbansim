# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable

class ln_income_x_ln_avg_val_per_unit_residential(Variable):
    """ """
    _return_type="float32"
    ln_residential_value_per_unit = "ln(urbansim.zone.avg_val_per_unit_residential)"
    hh_ln_income = "ln_bounded(urbansim.household.income)"
    
    def dependencies(self):
        return ["%s" % self.ln_residential_value_per_unit,
                "%s" % self.hh_ln_income]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_ln_income, 
                        self.ln_residential_value_per_unit)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from math import log
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.ln_income_x_ln_avg_val_per_unit_residential"

    def test_my_inputs(self):
        avg_value = array([10, 100, 0])
        income = array([1000, 300000, 50000, 0, 10550])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "avg_val_per_unit_residential":avg_value},
             "household":{ 
                 "income":income}
                     }, 
            dataset = "household_x_zone")
        should_be = array([[log(1000)*log(10),log(1000)*log(100), 0], 
                           [log(300000)*log(10),log(300000)*log(100), 0 ], 
                           [log(50000)*log(10),log(50000)*log(100), 0], 
                           [0,0,0], 
                           [log(10550)*log(10), log(10550)*log(100), 0]])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()