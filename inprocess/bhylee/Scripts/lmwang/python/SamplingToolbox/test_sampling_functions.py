import unittest
import time
import configure_path
from numarray import array, asarray, arange, concatenate, zeros, ones, \
     sometrue, where, equal, not_equal, nonzero, NumArray, \
     reshape, sum, cumsum, sort, searchsorted, repeat, argsort, \
     Float32
from numarray.random_array import randint, seed, uniform, random
from sampling_functions import *

class SampleFunctionsTest(unittest.TestCase):
    def test_SampleReplace(self):
        n = 200; size = 200
        a = arange(n)
        s = SampleReplace(a,size)
        self.assertEqual(len(s), size, msg ="sampled size not equal to size parameter")
        self.assert_( min(a) <= min(s) <= max(a), "sampled elements not in between min and max of source array")
        assert min(a) <= max(s) <= max(a), "sampled elements not in between min and max of source array"        
        
    def test_SampleNoReplace(self):
        n = 200; size = 200
        a = arange(n)
        s = SampleNoReplace(a,size)
        self.assertEqual(len(s), size, msg ="sampled size not equal to size parameter")
        assert min(a) <= min(s) <= max(a), "sampled elements not in between min and max of source array"
        assert min(a) <= max(s) <= max(a), "sampled elements not in between min and max of source array"        


    def test_ProbSampleReplace(self):
        n = 20000; size = 5000
        a = arange(n)
        p = 1/float(n)
        prob = repeat(array([p], typecode = Float32), n)

        start_time = time.time()
        s = ProbSampleReplace(a,size,prob)
        print "prob sample %s/%s w/o searchsorted(replace):" % (size,n) + str(time.time() - start_time)
        self.assertEqual(len(s), size, msg ="sampled size not equal to size parameter")
        assert min(a) <= min(s) <= max(a), "sampled elements not in between min and max of source array"
        assert min(a) <= max(s) <= max(a), "sampled elements not in between min and max of source array"
        #print s


    def test_ProbSampleReplaceL(self):
        n = 20000; size = 5000
        a = arange(n)
        p = 1/float(n)
        prob = repeat(array([p], typecode = Float32), n)

        start_time = time.time()
        s = ProbSampleReplaceL(a,size,prob)
        print "prob sample %s/%s w/ searchsorted(replace):" % (size,n) + str(time.time() - start_time)
        self.assertEqual(len(s), size, msg ="sampled size not equal to size parameter")
        assert min(a) <= min(s) <= max(a), "sampled elements not in between min and max of source array"
        assert min(a) <= max(s) <= max(a), "sampled elements not in between min and max of source array"        
        #print s

    def test_ProbSampleNoReplace(self):
        n = 20000; size = 5000
        a = arange(n)
        p = 1/float(n)
        prob = repeat(array([p], typecode = Float32), n)

        start_time = time.time()
        s = ProbSampleNoReplace(a,size,prob)
        print "prob sample %s/%s w/o searchsorted (no replace):" % (size,n)  + str(time.time() - start_time)
        self.assertEqual(len(s), size, msg ="sampled size not equal to size parameter")
        assert min(a) <= min(s) <= max(a), "sampled elements not in between min and max of source array"
        assert min(a) <= max(s) <= max(a), "sampled elements not in between min and max of source array"
        #print s

    def test_sample_1d_array_of_non_repeat_random_num(self):
        n = 20000; size = 5000
        a = arange(n)
        p = 1/float(n)
        prob = repeat(array([1], typecode = Float32), n)

        start_time = time.time()
        s = sample_1d_array_of_non_repeat_random_num(a,size,weight_array=prob)
        print "prob sample %s/%s w/ searchsorted (no replace):" % (size,n) + str(time.time() - start_time)
        self.assertEqual(len(s), size, msg ="sampled size not equal to size parameter")
        assert min(a) <= min(s) <= max(a), "sampled elements not in between min and max of source array"
        assert min(a) <= max(s) <= max(a), "sampled elements not in between min and max of source array"
        #print s
        

if __name__ == "__main__":
    unittest.main()
