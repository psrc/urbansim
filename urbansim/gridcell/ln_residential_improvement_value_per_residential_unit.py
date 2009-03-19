# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class ln_residential_improvement_value_per_residential_unit(Variable):
    """Natural log of the residential_improvement_value_per_residential_unit for this gridcell"""
    
    _return_type="float32"            
    residential_improvement_value = "residential_improvement_value"
    residential_units = "residential_units"

    def dependencies(self):
        return [my_attribute_label(self.residential_improvement_value), 
                my_attribute_label(self.residential_units)]

    def compute(self, dataset_pool):
        ru = self.get_dataset().get_attribute(self.residential_units)
        return ln_bounded(self.get_dataset().get_attribute(self.residential_improvement_value) /
                          ma.masked_where(ru==0.0, ru.astype(float32)))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        residential_improvement_value = array([50, 75, 0, 50, -20, 10000000000000000])
        residential_units = array([25, 50, 50, 50, 60, 1])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4,5,6]),
                    "residential_improvement_value":residential_improvement_value, 
                    "residential_units":residential_units
                }
            }
        )
        
        should_be = array([0.69314718, 0.4054651, 0.0, 0.0, 0.0, 36.8413614])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()