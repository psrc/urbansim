# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32
from opus_core.logger import logger

class average_residential_value_per_housing_unit(Variable):
    """Average residential value per housing units, computed by dividing the 
    total residential valueby the number of residential units"""

    total_residential_value = "total_residential_value"
    housing_units = "residential_units"

    def dependencies(self):
        return [my_attribute_label(self.total_residential_value), 
                my_attribute_label(self.housing_units)]

    def compute(self, dataset_pool):
        units = self.get_dataset().get_attribute(self.housing_units)
        return ma.filled(self.get_dataset().get_attribute(self.total_residential_value)/ 
                                       ma.masked_where(units == 0, units.astype(float32)),0.0)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", ma.filled(values,0.0))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        total_residential_value = array([1000, 5000, 10000, 15000])
        housing_units = array([0.0, 10.0, 300.0, 56.0])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id": array([1,2,3,4]),
                    "total_residential_value":total_residential_value, 
                    "residential_units":housing_units
                } 
            }
        )
        
        should_be = array([0.0, 500.0, 10000/300.0, 15000/56.0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
        
if __name__=='__main__':
    opus_unittest.main()
