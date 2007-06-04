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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class ln_price_SSS_times_ln_price_vacant_land(Variable):
    """Multiplication of two zone variables"""

    _return_type = "float32"
    
    price_vacant_land = "ln_avg_val_per_unit_vacant_land"
    
    def __init__(self, type):
        self.price = "ln_avg_val_per_unit_%s" % type
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.price), 
                 my_attribute_label(self.price_vacant_land)]
    
    def compute(self, dataset_pool):
        p = self.get_dataset().get_attribute(self.price)
        vp = self.get_dataset().get_attribute(self.price_vacant_land)
        return (p-p.mean()) * (vp-vp.mean())


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.ln_price_residential_times_ln_price_vacant_land"

    def test_my_inputs(self):
        price_residential = array([21,22,3,42]) 
        price_vacant_land = array([2,3,4.5,0])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                 "ln_avg_val_per_unit_residential": price_residential,
                 "ln_avg_val_per_unit_vacant_land": price_vacant_land
                 },
             },
            dataset = "zone")
        
        should_be = array([(21-22)*(2-2.375), 0, (3-22)*(4.5-2.375), (42-22)*(-2.375)])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-10), True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()