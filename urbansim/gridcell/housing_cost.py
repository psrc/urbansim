# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class housing_cost(Variable):
    """housing_cost = (residential_land_value + residential_improvement_value)/residential_units/property_value_to_annual_cost_ratio"""
    
    total_residential_value = "total_residential_value"
    residential_units = "residential_units"

    def dependencies(self):
        return [my_attribute_label(self.total_residential_value),
                my_attribute_label(self.residential_units)]

    def compute(self, dataset_pool):
        units = self.get_dataset().get_attribute(self.residential_units)
        return ma.filled(self.get_dataset().get_attribute(self.total_residential_value) / 
                ma.masked_where(units == 0, units.astype(float32)) / 
                dataset_pool.get_dataset('urbansim_constant')["property_value_to_annual_cost_ratio"], 0.0)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        ratio = 10.3        
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4,5,6]),
                    'total_residential_value': array([50, 75, 0, 5, 20.5, 10000000000000000]),
                    'residential_units': array([1, 1, 0, 0, 2, 100]),
                },
                'urbansim_constant':{
                    "property_value_to_annual_cost_ratio": array([ratio]),
                }
            }
        )
        
        should_be = array([50./1/ratio, 75./1/ratio, 0, 0, 20.5/2/ratio, 10000000000000000./100/ratio])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
        
if __name__=='__main__':
    opus_unittest.main()