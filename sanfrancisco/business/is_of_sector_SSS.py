# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
    
class is_of_sector_SSS(Variable):
    """is business of sector name SSS """

    def __init__(self, sector_name):
        self.sector_name = sector_name.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return ["sector_name=business.disaggregate(sector.sector_name)"]
        
    def compute(self,  dataset_pool):
        return  self.get_dataset().get_attribute("sector_name") == self.sector_name

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
            'business':
            {"business_id":array([1,2,3,4,5]),
             "sector_id":array([4,2,4,3,4])
             },
            'sector':
            {"sector_id":array([1,2,3,4]),
             "sector_name":array(["others","agr","manufactural","retail"])
             },
             
           }
        )
        
        should_be = array([1, 0, 1, 0, 1])
        instance_name = 'sanfrancisco.business.is_of_sector_retail'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
