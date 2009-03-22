# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class parcel_id(Variable):
    """The parcel_id of business."""

    gc_parcel_id = "parcel_id"
    
    def dependencies(self):
        return ["_parcel_id=business.disaggregate(building.parcel_id)"
                ]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_parcel_id")

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
            'building':
            {"building_id":array([1,2,3,4,5]),
             "parcel_id":array([1,1,2,3,5])
             },
            'business':
            {"business_id":array([1,2,3,4,5]),
             "building_id":array([1,1,2,3,7])
             },
             
           }
        )
        
        should_be = array([1, 1, 1, 2, -1])
        instance_name = 'sanfrancisco.business.parcel_id'
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()



#from opus_core.tests import opus_unittest
#from opus_core.datasets.dataset_pool import DatasetPool
#from opus_core.storage_factory import StorageFactory
#from numpy import array
#from opus_core.tests.utils.variable_tester import VariableTester
#
#class Tests(opus_unittest.OpusTestCase):
#    def test_my_inputs(self):
#        tester = VariableTester(
#            __file__,
#            package_order=['sanfrancisco','urbansim'],
#            test_data={
#            'business':
#            {"business_id":array([1,2,3,4,5]),
#             "building_id":array([4,2,4,3,4])
#             },
#            'building':
#            {"building_id":array([1,2,3,4]),
#             "parcel_id":array(["others","agr","manufactural","retail"])
#             },
#             
#           }
#        )
#        
#        should_be = array([1, 0, 1, 0, 1])
#        instance_name = 'sanfrancisco.business.is_of_sector_retail'
#        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, instance_name)
#
#if __name__=='__main__':
#    opus_unittest.main()
