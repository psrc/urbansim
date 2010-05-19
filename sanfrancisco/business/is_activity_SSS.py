# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import array
    
class is_activity_SSS(Variable):
    """
    ## building use has been renamed to activity
    is business of activity_name SSS (cie, med, mips, pdr, retailent, visitor).
    """

    def __init__(self, activity_name):
        self.activity_name = activity_name.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return [
               "sanfrancisco.business.activity_name"
               ]
        
    def compute(self,  dataset_pool):
        activity_names = self.get_dataset().get_attribute("activity_name")
        return  activity_names == self.activity_name

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
             "activity_id":array([1,2,1,3,1]),
#             "building_use":  strarray.array(["cie", "mips", "cie", "pdr", "cie"]),
             },
            'activity':
            {"activity_id":array([1,2,3]),
             "activity_name":  array(["cie", "mips", "pdr"]),
             },
           }
        )
        
        should_be = array([1, 0, 1, 0, 1])
        instance_name = 'sanfrancisco.business.is_activity_cie'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
