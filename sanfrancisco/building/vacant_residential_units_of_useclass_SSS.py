# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_residential_units_of_useclass_SSS(Variable):
    """Number of vacant residential units in buildings of the given use classification"""

    _return_type="int32"
    
    def __init__(self, useclass):
        self.useclass = useclass.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return ["_vacant_residential_units_of_useclass_%s =  where ( sanfrancisco.building.building_class_name=='%s', sanfrancisco.building.residential_units - sanfrancisco.building.number_of_households,0)" 
                % (self.useclass,self.useclass)]
 
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_vacant_residential_units_of_useclass_%s" % self.useclass)

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("residential_units").max()
        self.do_check("x >= 0 and x <= " + str(size), values)
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from numpy import array, alltrue
from opus_core.tests.utils.variable_tester import VariableTester
from sanfrancisco.datasets.building_use_classification_dataset import BuildingUseClassificationDataset
from sanfrancisco.datasets.building_use_dataset import BuildingUseDataset
from sanfrancisco.datasets.building_dataset import BuildingDataset
from urbansim.datasets.household_dataset import HouseholdDataset

class Tests(opus_unittest.OpusTestCase):
    variable_name = 'sanfrancisco.building.vacant_residential_units_of_useclass_classonetwo'

    def test_my_inputs(self):
        
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
                "building_use_classification":{
                    "class_id":array([1,2]),
                    "name":array(['classonetwo','classthreefour']),
                    },
                "building_use":{
                    "building_use_id":array([1,2,3,4]),
                    "class_id":array([1,1,2,2])
                    },
                    # buildings 1, 3, 4 are in class34, buildings 2,5,6 in class12
                 "building":{
                     "building_id":array([1,2,3,4,5,6]),
                     "building_use_id":array([3,1,4,3,2,1]),
                     "residential_units":array([11,12,13,14,15,16])
                    },
                    # 5 households in building 1,2,3; 3 households in building 3,4,5
                 "household":{
                      "building_id":array([1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,5,5,5,6,6,6])
                    }
                    # => 6,7,8,11,12,13 vacant units in buildings, respectively
                    # => 6+8+11 = 25 in class34, 7+12+13 = 32 in class12
           }
        )

        values = tester._get_attribute(self.variable_name)
        print values
        
        should_be = array([0, 7, 0, 0, 12, 13])
        tester.test_is_equal_for_family_variable(self, should_be, self.variable_name)
        
#        test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
