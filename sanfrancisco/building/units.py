# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, zeros
from opus_core.misc import unique
import re
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class units(Variable):
    """Return the measure of units for the buildings, such as non_residential_sqft or residential units, depending on the the unit_name column of building types. 
    e.g. return non_residential_sqft for buildings the unit_name of its building type is "non_residential_sqft", and residential_units for "residential_units", etc
    """
    _return_type="int32"
    
    def dependencies(self):
        return ['sanfrancisco.building_type.unit_name',
                "unit_name=building.disaggregate(building_type.unit_name)"
                ]
        
    def compute(self,  dataset_pool):
        bldg = self.get_dataset()
        bt = dataset_pool.get_dataset("building_type")
        results = zeros(bldg.size(), dtype = self._return_type)
        for unit_name in unique(bt.get_attribute('unit_name')):
            self.add_and_solve_dependencies("sanfrancisco.building.%s" % unit_name, dataset_pool)
            is_of_this_unit_name = bldg.get_attribute('unit_name')==unit_name
            results[is_of_this_unit_name] = bldg.get_attribute(unit_name)[is_of_this_unit_name].astype(self._return_type)
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
            'building_type':
            {
                "building_type_id":array([1,2,3,4]),
                "class_id":array([1,2,1,2]),
                },
            'building_type_classification':
            {
                "class_id":array([1,2]),
                "name": array(["nonresidential","residential"]),
                "unit_name":array(["building_sqft","residential_units"])                
                },           
            "building":{
                'building_id': array([1, 2, 3, 4, 5]),
                'building_type_id': array([1, 2, 3, 4, 3]),
                'building_sqft': array([1000, 200, 0, 400, 1500]),
                'residential_units': array([0, 2, 0, 40, 5]),                
                },
        }
        )
        
        should_be = array([1000, 2, 0, 40, 1500])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()