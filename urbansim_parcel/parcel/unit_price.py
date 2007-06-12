#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
from numpy import ma
from numpy import float32

class unit_price(Variable):
    """ (land_value + improvement_value) / residential_units."""
    
    land_value = "land_value"
    improvement_value = "improvement_value"
    
    def dependencies(self):
        return ["_unit_price = (parcel.land_value + parcel.improvement_value) / urbansim_parcel.parcel.existing_units"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_unit_price")

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)
        
from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    ACRE = 43560
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "land_value": array([1,   2,    3 ]),
                "improvement_value": array([1, 50,  200]),
                "existing_units": array([1,   2,    3 ]),                
            },        })
        should_be = array([2, 26, 67])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
