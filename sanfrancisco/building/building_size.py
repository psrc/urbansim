# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, zeros
import re
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class building_size(Variable):
    """Return size of the building, either sqft, or residential units, depending on the building type. 
    If the value in column 'units' of the building_types table contains a substring 'sqft', it will take 
    the 'sqft' of the buildings table as a measure of size, otherwise 'residential_units'.
    """
    _return_type="int32"
    
    def dependencies(self):
        return [my_attribute_label("building_sqft"), 
                my_attribute_label("residential_units"),
                "unit_name=building_use.disaggregate(building_use_classification.units)",
                "unit_name=building.disaggregate(building_use.unit_name)",  
                ]
        
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()        
        bc = dataset_pool.get_dataset("building_use_classification")
        results = zeros(buildings.size(), dtype = self._return_type)
        for unit_name in bc.get_attribute("units"):
            idx = where(buildings.get_attribute('unit_name') == unit_name)[0]
            results[idx] = buildings.get_attribute_by_index(unit_name, idx).astype(self._return_type)
        return results

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array, arange
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
                "name": array(["nonresidential","residential"]),
                "units":array(["building_sqft","residential_units"])                
                },           
            "building":{
                'building_id': array([1, 2, 3, 4, 5]),
                'building_use_id': array([1, 2, 3, 4, 3]),
                'building_sqft': array([1000, 200, 0, 400, 1500]),
                'residential_units': array([0, 2, 0, 40, 5]),                
                },
        }
        )
        
        should_be = array([1000, 2, 0, 40, 1500])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()