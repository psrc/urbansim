# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import float32

class attr_test_family_DDD(Variable):
    """A variable for unit tests.
    """ 
    _return_type="float32"
    
    def __init__(self, number):
        self.tnumber = number
        Variable.__init__(self)
    
    def dependencies(self):
        return ['opus_core.test.attr1']
        
    def compute(self, dataset_pool):
        values = self.get_dataset().get_attribute('attr1') * self.tnumber
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
                'test':{
                    'id': array([1, 2]),
                    'attr1': array([1, 2]),
                    },
            }
        )
        
        should_be = array([1*32, 2*32])
        instance_name = 'opus_core.test.attr_test_family_32'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()