# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class number_of_households(Variable):
    """Number of households in a given building"""

    _return_type="int32"
    
    def dependencies(self):
        return ["_number_of_households=building.number_of_agents(household)"]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_households")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("household").size()
        self.do_check("x >= 0 and x <= " + str(size), values)

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
                    # 5 households in building 1,2,3; 3 households in building 3,4,5
                 "household":{
                      "building_id":array([1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,5,5,5,6,6,6])
                    }
                    # => 6,7,8,11,12,13 vacant units in buildings, respectively
                    # => 6+8+11 = 25 in class34, 7+12+13 = 32 in class12
           }         
        )
        
        should_be = array([5, 5, 5, 3, 3, 3])
        assert(alltrue(should_be==tester._get_attribute()))
#        test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
