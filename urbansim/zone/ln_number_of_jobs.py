#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.variables.variable import Variable, ln_bounded
from urbansim.functions import attribute_label

class ln_number_of_jobs(Variable):
    """ln of number_of_jobs
    """
    
    def dependencies(self):
        return [attribute_label("zone", "number_of_jobs")]
    
    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute('number_of_jobs'))

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array, log
from numpy import ma
import math

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.ln_number_of_jobs"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(
            self.variable_name, {
                "zone":{
                    "zone_id":array([1,2, 3])}, 
                "gridcell":{
                    "number_of_jobs":array([1,2,3,5]),
                    "zone_id":array([1,2,1,3]) , 
                    "grid_id":array([1,2,3,4])}, 
                "job":{
                    "job_id":array([1,2,3,4,5,6,7,8,9,10,11]), 
                    "grid_id":array([1,2,2,3,3,3,4,4,4,4,4])},
                }, 
            dataset = "zone")
        should_be = log(array([4,2, 5]))
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2),
                         True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()