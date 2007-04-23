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
from urbansim.functions import attribute_label
from numpy import zeros, where

class nonresidential_building_sqft(Variable):
    """total building_sqft in nonresidential class. """
   
    _return_type="int32"
    
    def dependencies(self):
        return [my_attribute_label("building_sqft"), 
                "_class_name=building_use.disaggregate(building_use_classification.name)",
                "_class_name=building.disaggregate(building_use._class_name)",
            ]
        
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        results = zeros(buildings.size(), dtype=self._return_type)
        w = where(buildings.get_attribute("_class_name")=="nonresidential")[0]
        results[w] = buildings.get_attribute("building_sqft")[w]
        return results

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'building_use':
            {
                "building_use_id":array([1,2,3,4]),
                "class_id":array([1,2,1,2]),
                },
            'building_use_classification':
            {
                "class_id":array([1,2]),
                "name":    array(["nonresidential","residential"])
                },           
            "building":{
                'building_id': array([1, 2, 3, 4, 5]),
                'building_use_id': array([1, 2, 3, 4, 3]),
                'building_sqft': array([1000, 200, 0, 400, 1500]),
                },
        }
        )
        
        should_be = array([1000, 0, 0, 0, 1500])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
       