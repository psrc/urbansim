# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class building_class_id(Variable):
    """The class name (residential, nonresidential) of this building. """
   
    def dependencies(self):
        return ["_building_class_id=building.disaggregate(building_use_classification.class_id, intermediates=[building_use])"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_building_class_id")
    
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
                "building_use_classification":{
                    "class_id":array([1,2]),
                    "class_name":array(['residential','nonresidential']),
                    },
                "building_use":{
                    "building_use_id":array([1,2,3,4]),
                    "class_id":array([1,1,2,2])
                    },
                 "building":{
                     "building_id":array([1,2,3,4,5,6]),
                     "building_use_id":array([3,1,4,3,2,1]),
                 }             
           }
        )
        
        should_be = array([2,1,2,2,1,1])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
