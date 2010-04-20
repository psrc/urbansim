# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class average_income(Variable):
    """average income in a given zone"""

    _return_type="int32"
    
    def dependencies(self):
        return ["sanfrancisco.household.zone_id", 
                "_average_income=zone.aggregate(household.income, function=mean)"
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_average_income")

    def post_check(self,  values, dataset_pool=None):
        imin = dataset_pool.get_dataset("household").get_attribute("income").min()
        imax = dataset_pool.get_dataset("household").get_attribute("income").max()
        self.do_check("x >= %s and x <= %s" % (imin, imax), values)

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
                "household":{
                    "household_id":array([1,2,3,4,5,6,7,8,9,10]),
                    "income":array([11,12,13,14,15,16,17,18,19,20]),
                    "zone_id":array([1,2,1,2,1,2,1,2,1,3]),
                    },
                "zone":{
                    "zone_id":array([1,2,3,4])
                    }
                # zone 1: 11,13,15,17,19 = 15
                # zone 2: 12,14,16,18 = 15
                # zone 3: 20 = 20
           }
        )
        
        should_be = array([15, 15, 20, 0])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
