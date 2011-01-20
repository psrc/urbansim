# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class total_annual_rent(Variable):
    """Total annual rent as computed by dividing the total residential value of the gridcell
    by the number of residential units, and then dviding that figure by the 
    property value to annual cost ratio."""
    _return_type="float32"
    total_residential_value = "total_residential_value"
    residential_units = "residential_units"

    def dependencies(self):
        return [my_attribute_label(self.total_residential_value), 
                my_attribute_label(self.residential_units)]

    def compute(self, dataset_pool):
        ru = self.get_dataset().get_attribute(self.residential_units)
        return self.get_dataset().get_attribute(self.total_residential_value) / \
               ma.masked_where(ru==0.0, ru.astype(float32)) / \
               dataset_pool.get_dataset('urbansim_constant')["property_value_to_annual_cost_ratio"]



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3]),
                    'residential_units': array([25, 50, 75]),
                    'total_residential_value': array([10000, 10002, 300]),
                    },
                'urbansim_constant':{
                    'property_value_to_annual_cost_ratio': array([50]),
                }
            }
        )
        
        should_be = array([8.0, 4.0007996559, 0.0799999982])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()