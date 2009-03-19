# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class acres_per_gridcell(Variable):
    """total acres of land for a given gridcell (ignoring percent water).  This is also available in urbansim_constants; it is defined
    as a variable so that it can be used in an expression"""

    _return_type = "float32"

    def dependencies(self):
        return [my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        return 0*self.get_dataset().get_attribute("grid_id") + dataset_pool.get_dataset('urbansim_constant')["acres"]


from numpy import array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3]),
                },
                'urbansim_constant':{
                    "acres": array([105.0]),
                }
            }
        )
        
        should_be = array([105.0, 105.0, 105.0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
