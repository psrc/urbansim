#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

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