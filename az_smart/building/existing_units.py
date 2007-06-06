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
from numpy import zeros, where
from opus_core.misc import unique_values

class existing_units(Variable):
    """total number of units (residential_units or sqft, defined in building_types) """
    _return_type = "int32"
    
    def dependencies(self):
        return ["_unit_name=building.disaggregate(building_type.unit_name)",
                "parcel_sqft=building.disaggregate(parcel.parcel_sqft)",
                "az_smart.building.building_sqft",
                "az_smart.building.residential_units"
                ]
        
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        results = zeros(buildings.size(),dtype=self._return_type)
        unit_names = buildings.get_attribute("_unit_name")
        unique_unit_names = unique_values(unit_names)
        for unit_name in unique_unit_names:
            if unit_name.strip() == '':continue
            uw = where(unit_names == unit_name)[0]
            results[uw] = buildings.get_attribute(unit_name)[uw].astype(self._return_type)
        return results
    
    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)
            
from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['az_smart','urbansim'],
            test_data={
            'building':
            {
                'building_id': array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                'building_type_id':array([1, 1, 1, 1, 2, 2, 2, 3, 3, 3]),
                'parcel_id':       array([1, 1, 2, 3, 1, 2, 3, 4, 4, 4]),
                'residential_units': array([7, 2, 3, 0, 2, 3, 4, 1, 0, 0]),
                'building_sqft': array([19, 2000, 310, 400, 27, 223, 58, 0, 0, 0])               
                },           
            "building_type":{
                'building_type_id':  array([1, 2, 3]),
                'unit_name':         array(['building_sqft', 'residential_units', 'parcel_sqft'])
            },
            "parcel":{
                'parcel_id':   array([1, 2, 3, 4]),
                'parcel_sqft': array([1000, 3000, 4000, 3400])
            },                    
        }
        )
        
        should_be = array([19, 2000, 310, 400, 2, 3, 4, 3400, 3400, 3400])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    