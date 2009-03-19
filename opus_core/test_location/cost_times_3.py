# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from numpy import float32

class cost_times_3(Variable):
    """A variable for unit tests.
    """ 
    _return_type="float32"
        
    def dependencies(self):
        return ['opus_core.test_location.cost']
        
    def compute(self, dataset_pool):
        values = self.get_dataset().get_attribute('cost') * 3
        return values
        

from numpy import array

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test(self):
        tester = VariableTester(
            __file__,
            package_order=['opus_core'],
            test_data={
                'test_location':{
                    'id': array([1, 2]),
                    'cost': array([25, 40]),
                    },
            }
        )
        
        should_be = array([75, 120])
        
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()