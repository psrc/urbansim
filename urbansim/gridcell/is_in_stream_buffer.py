# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_in_stream_buffer(Variable):
    """Returns a boolean indicating if the gridcell is in a stream buffer"""

    percent_stream_buffer = "percent_stream_buffer"

    def dependencies(self):
        return [my_attribute_label(self.percent_stream_buffer)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.percent_stream_buffer) > \
                                       dataset_pool.get_dataset('urbansim_constant')["percent_coverage_threshold"]

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


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
                    'percent_stream_buffer': array([25, 50, 75]),
                    },
                'urbansim_constant':{
                    'percent_coverage_threshold': array([50]),
                }
            }
        )
        
        should_be = array([False, False, True])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()