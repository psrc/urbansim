# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class zone_id(Variable):
    """The taz id of this household. """
   
    def dependencies(self):
        return ["_zone_id=household.disaggregate(parcel.zone_id, intermediates=[building])"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_zone_id")

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
            'parcel':
            {"parcel_id":array([1,2,3,4,5]),
             "zone_id":  array([2,1,2,3,1]),
             },
            'building':
            {"building_id":array([1,2,3,4,5]),
             "parcel_id":array([1,1,2,3,5])
             },
            'household':
            {"household_id":array([1,2,3,4,5]),
             "building_id":array([1,1,2,3,7])
             },
             
           }
        )
        
        should_be = array([2, 2, 2, 1, -1])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
