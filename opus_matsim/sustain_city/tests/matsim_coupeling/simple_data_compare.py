# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

from opus_core.tests import opus_unittest
from numpy import array, zeros, int8, arange
from opus_core.logger import logger

class SimpleDataCompare(opus_unittest.OpusTestCase):
    """ This test validates the generated xml MATSim configuration while using pyxb's own validation process.
    """
    
    def setUp(self):
        print "Entering setup"
        
        logger.log_status('Executing sample numpay array comparison tests...')
        
        print "Leaving setup"
    
    def test_run(self):
        print "Entering test run"

        self.test1()
        self.test2()
        
        print "Leaving test run"
        
    def test1(self):
        # create test array
        test_array1 = array([[1,2,3],[4,5,6], [7,8,9]], dtype=int8)
        test_array2 = zeros((3, 4), dtype=int8)
        
        # compare matrices (shouldn't be true)
        self.assertFalse( test_array1==test_array2 )
        
    def test2(self):
        # create test array
        test_array1 = arange( 9 ).reshape(3,3)
        test_array2 = array([[0,1,2],[3,4,5], [6,7,8]], dtype=test_array1.dtype.name)
        
        result = (test_array1==test_array2)
        result2= result.all()
        
        # compare matrices (shouldn't be true)
        self.assertTrue( result2 )
        
if __name__ == "__main__":
    opus_unittest.main()