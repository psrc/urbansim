# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class acres_of_land(Variable):
    """Acres of land for a given gridcell, based on the
    water percentage for that given gridcell"""

    _return_type = "float32"
    percent_water = "percent_water"

    def dependencies(self):
        return [my_attribute_label(self.percent_water)]

    def compute(self, dataset_pool):
        return (1.0-(self.get_dataset().get_attribute(self.percent_water)/100.0)) * \
                    dataset_pool.get_dataset('urbansim_constant')["acres"]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

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
                    'percent_water': array([33, 5, 20]),
                },
                'urbansim_constant':{
                    "acres": array([105.0]),
                }
            }
        )
        
        should_be = array([(1.0 - (33/100.0))*105.0, 
                           (1.0 - (5/100.0))*105.0, 
                           (1.0 - (20/100.0))*105.0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
