# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class building_typeclass_name(Variable):
    """The typeclass name (single, mixed, industrial, etc) of this building. """
   
    def dependencies(self):
        return ["_building_typeclass_name=building.disaggregate(building_type_classification.name, intermediates=[building_type])"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_building_typeclass_name")
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array, alltrue
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
                "building_type_classification":{
                    "class_id":array([1,2]),
                    "name":array(['apartment','hotel']),
                    },
                "building_type":{
                    "building_type_id":array([1,2,3,4]),
                    "class_id":array([1,1,2,2])
                    },
                 "building":{
                     "building_id":array([1,2,3,4,5,6]),
                     "building_type_id":array([3,1,4,3,2,1]),
                 }             
           }
        )
        
        should_be = array(['hotel','apartment','hotel','hotel','apartment','apartment'])
        print(tester._get_attribute())

        assert(alltrue(should_be==tester._get_attribute()))
#        test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()