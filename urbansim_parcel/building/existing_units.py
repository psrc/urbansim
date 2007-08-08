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
from numpy import zeros, logical_not
from opus_core.misc import unique_values

class existing_units(Variable):
    """total number of units (residential_units or sqft, defined in building_types) """
    _return_type = "int32"
    
    def dependencies(self):
        return [
                "urbansim_parcel.building.building_sqft",
                "urbansim_parcel.building.residential_units",
                "urbansim_parcel.building.are_units_building_sqft"
                ]
        
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        result = zeros(buildings.size(),dtype=self._return_type)
        is_sqft = buildings.get_attribute("are_units_building_sqft")
        residential_units = buildings.get_attribute("residential_units")
        where_residential = logical_not(is_sqft)
        result[where_residential] = residential_units[where_residential].astype(self._return_type)
        result[is_sqft] = buildings.get_attribute("building_sqft")[is_sqft].astype(self._return_type)
        return result
    
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
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            'building':
            {
                'building_id': array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                'residential_units':    array([0,   2,   3,   0,   2,   3,  4, 1, 0, 5]),
                'sqft_per_unit':        array([0,   2,   2,   0,   10,  5,  2,20, 0, 20]),
                'non_residential_sqft': array([19,  0, 310, 400,   0, 223, 58, 0, 0, 0])               
                },           
        }
        )
        
        should_be = array([19, 2, 316, 400, 2, 223+15, 8+58, 1, 0, 5])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    
