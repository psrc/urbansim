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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class building_sqft_per_unit(Variable):
    """ (building_sqft) / residential_units."""
    
    _return_type="float32"
    
    def dependencies(self):
        return ["_building_sqft_per_unit = parcel.building_sqft / parcel.residential_units"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_building_sqft_per_unit")

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'parcel':{
                     "parcel_id":array([1,2,3,4,5]),
                     "residential_units":array([2,0,1,4,7]),
                     "building_sqft":array([1000,3000,2000,1005,7000]),             
                     }
            }
        )
        
        should_be = array([500, 0, 2000, 251, 1000])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
