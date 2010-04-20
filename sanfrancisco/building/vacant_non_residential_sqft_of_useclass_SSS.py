# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_non_residential_sqft_of_useclass_SSS(Variable):
    """Number of vacant residential units in buildings of the given use classification"""

    _return_type="int32"
    
    def __init__(self, useclass):
        self.useclass = useclass.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return ["_vacant_non_residential_sqft_of_useclass_%s =  where ( sanfrancisco.building.building_class_name=='%s', sanfrancisco.building.non_residential_sqft - sanfrancisco.building.number_of_business_occupied_sqft,0)" 
                % (self.useclass,self.useclass)]
 
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_vacant_non_residential_sqft_of_useclass_%s" % self.useclass)

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("non_residential_sqft").max()
        self.do_check("x >= 0 and x <= " + str(size), values)
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from numpy import array, alltrue
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    variable_name = 'sanfrancisco.building.vacant_non_residential_sqft_of_useclass_med'

    def test_my_inputs(self):
        
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
                "building_use_classification":{
                    "class_id":array([1,2]),
                    "name":array(['cie','med']),
                    },
                "building_use":{
                    "building_use_id":array([1,2,3,4]),
                    "class_id":array([1,1,2,2])
                    },
                    # buildings 1, 3, 4 are in class34, buildings 2,5,6 in class12
                 "building":{
                     "building_id":array([1,2,3,4,5,6]),
                     "building_use_id":array([3,1,4,3,2,1]),
                     "non_residential_sqft":array([1000,2000,3000,4000,5000,6000])
                    },
                    # 5 business in building 1,2,3; 3 business in building 3,4,5
                 "business":{
                      "business_id":array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]),
                      "building_id":array([1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,5,5,5,6,6,6]),
                      "sqft":array([1,2,3,4,5,
                                    6,7,8,9,10,
                                    11,12,13,14,15,
                                    16,17,18,
                                    19,20,21,
                                    22,23,24]),
                    }
           }
        )
        # med = building_use 3 and 4, or buildings 1,3 and 4, which have 1000, 3000, 4000 sqft
        #       but business 1-5, 11-15, 16-18 are in there, using up
        #        15, 65 and 51 sqft = 135 sqft
        #       => vacant = 985, 2935 and 3949 sqft respectively

        values = tester._get_attribute(self.variable_name)
        print values
        
        should_be = array([985, 0, 2935, 3949, 0, 0])
        tester.test_is_equal_for_family_variable(self, should_be, self.variable_name)
        
#        test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
