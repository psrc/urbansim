# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_DDD_units(Variable):
    """Boolean indicating whether the parcel has DDD residential units"""

    residential_units = "residential_units"

    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number

    def dependencies(self):
        return [my_attribute_label(self.residential_units)]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute(self.residential_units) == self.tnumber

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x == True or x == False", values)


from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
                "parcel":{
                          "parcel_id":array([1,2,3]),
                          "residential_units":array([0, 2, 1]),                
                          }
            }
        )
        should_be = array([False, True, False])
        instance_name = "urbansim_parcel.parcel.has_2_units"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()