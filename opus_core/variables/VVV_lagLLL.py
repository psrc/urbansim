# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.lag_variable import LagVariable

class VVV_lagLLL(LagVariable):
    """A built-in class used to implement lag variables.
    Returns a set of rows with the same set of ids as exist in the current
    year's dataset for this variable.  Rows with ids that existed in the prior
    year but not in the the current year are removed.  Rows with ids that 
    did not exist in the prior year but do exist in the current year are
    added, and given the value from the current year.
    """
    
import os
from opus_core.tests import opus_unittest
    
class VVV_lagLLLTests(opus_unittest.OpusTestCase):
    """For addional lag variable tests, see:
    - psrc.tests.test_simulate_psrc
    - urbansim.gridcells.n_recent_transitions_to_developed
    """
    def test_lag_variable(self):
        from opus_core.variables.variable_factory import VariableFactory
        from opus_core.variables.variable_name import VariableName
        vf = VariableFactory()
        var_name = VariableName('opus_core.tests.a_test_variable_lag3')
        var = vf.get_variable(var_name, None, index_name='my_id')
        self.assert_(var.is_lag_variable())
        self.assertEqual(var.lag_offset, 3)

if __name__ == '__main__': 
    opus_unittest.main()
