# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln
from variable_functions import my_attribute_label

class ln_income(Variable):
    """Log of household income."""
    
    income = "income"
    
    def dependencies(self):
        return [my_attribute_label(self.income)]
    
    def compute(self, dataset_pool):    
        return ln(self.get_dataset().get_attribute(self.income))


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.ln_income"

    def test_my_inputs( self ):
        income = array([10000, 11000, 12000, 10000])

        values = VariableTestToolbox().compute_variable( self.variable_name, \
            {"household":{ \
                "income":income,
                }}, \
            dataset = "household" )
        should_be = array( [9.210340372,9.305650552,9.392661929,9.210340372] )
        
        self.assertEqual(ma.allclose( values, should_be, rtol=1e-7 ), \
                          True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()