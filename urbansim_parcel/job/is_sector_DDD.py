# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class is_sector_DDD(Variable):
    """whether the job is of sector id DDD."""

    def __init__(self, sector_id):
        self.sector_id = sector_id
        Variable.__init__(self)    
    
    def dependencies(self):
        return [my_attribute_label("sector_id")]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("sector_id") == self.sector_id

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
                "job":{
                    "job_id":array([1, 2, 3, 4, 5, 6, 7, 8]),
                    "sector_id":array([1, 2, 2, 2, 3, 3, 4, 5]),
                    },                 
           }
        )
        
        should_be = array([0, 1, 1, 1, 0, 0, 0, 0])
        instance_name = 'urbansim_parcel.job.is_sector_2'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
