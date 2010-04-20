# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class number_of_business_occupied_sqft(Variable):
    """Number of business_occupied_sqft in a given building"""

    _return_type="int32"
    
    def dependencies(self):
        return ["_number_of_business_occupied_sqft=building.aggregate(business.sqft)"]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_business_occupied_sqft")

    def post_check(self,  values, dataset_pool=None):
        # TODO
        # size = dataset_pool.get_dataset("household").size()
        self.do_check("x >= 0", values) #  and x <= " + str(size), values)

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
                 "building":{
                     "building_id":array([1,2,3,4,5,6]),
                     "building_use_id":array([3,1,4,3,2,1]),
                     "residential_units":array([11,12,13,14,15,16])
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
        
        should_be = array([15, 40, 65, 51, 60, 69])
        assert(alltrue(should_be==tester._get_attribute()))
#        test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
