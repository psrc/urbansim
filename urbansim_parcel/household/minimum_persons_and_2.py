# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import minimum
from opus_core.variables.variable import Variable

class minimum_persons_and_2(Variable):
    """minimum of persons and 2"""

    _return_type="int32"
    
    def dependencies(self):
        return ["household.persons"]

    def compute(self,  dataset_pool):
        return minimum(self.get_dataset().get_attribute("persons"), 2)
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={            
            'household':
            {
                'household_id': array([1,2,3,4]),
                'persons':      array([2, 1, 1, 7])
            },
            }
        )
        
        should_be = array([2, 1, 1, 2])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    