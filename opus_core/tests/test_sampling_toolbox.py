# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.sampling_toolbox import sample_replace
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.sampling_toolbox import probsample_replace
from opus_core.sampling_toolbox import probsample_noreplace
from opus_core.sampling_toolbox import find_duplicates
from opus_core.sampling_toolbox import prob2dsample
from opus_core.sampling_toolbox import sample_choice
from opus_core.tests import opus_unittest
import time
from numpy import array, arange
from numpy import sometrue, alltrue, not_equal, ndarray
from numpy import float32, all
from numpy.random import randint, seed
from opus_core.logger import logger

class SampleToolboxTest(opus_unittest.OpusTestCase):
    n = 200 #population size
    imin = 12; imax = 1500
    all = randint(imin, imax, n)  #population
    amin = all.min(); amax = all.max()
    size = 50 #sample size
    prob = all / float(all.sum())

    sample_size = (50, 10)  #sampel size for 2d sample

    def test_sample_replace(self):
        start_time = time.time()
        sample = sample_replace(self.all, self.size, return_index=True)
        logger.log_status("sample_replace %s from %s items array in " % (self.size,self.n) + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.size, self.size, msg ="sample size not equal to size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"

    def test_sample_noreplace(self):
        start_time = time.time()
        sample = sample_noreplace(self.all, self.size, return_index=True)
        logger.log_status("sample_noreplace %s from %s items array in " % (self.size,self.n) + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.size, self.size, msg ="sample size not equal to size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"
        assert not sometrue(find_duplicates(sample)), "there are duplicates in samples"

    def test_probsample_replace(self):
        start_time = time.time()
        sample = probsample_replace(self.all, self.size, self.prob, return_index=True)
        logger.log_status("probsample_replace %s from %s items array in " % (self.size,self.n) + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.size, self.size, msg ="sample size not equal to size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"
        assert alltrue(not_equal(self.prob[sample], 0.0)), "elements with zero weight in the sample"

    def test_probsample_noreplace(self):
        start_time = time.time()
        sample = probsample_noreplace(self.all, self.size, self.prob, return_index=True)
        logger.log_status("probsample_noreplace %s from %s items array in " % (self.size,self.n) + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.size, self.size, msg ="sample size not equal to size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"
        assert alltrue(not_equal(self.prob[sample], 0.0)), "elements with zero weight in the sample"
        assert not sometrue(find_duplicates(sample)), "there are duplicates in samples"

    def test_probsample_noreplace_ordering(self):
        probs=array([1, 1, 1, 1, 100, 1, 1, 1, 1, 1])
        probsum = float(probs.sum())
        first = []
        n = 100
        #seed(10)
        for i in range(n):
            sample = probsample_noreplace(arange(10), 5, prob_array=probs/probsum, return_index=False)
            # keep the first element sampled
            first.append(sample[0])
        # How many times the fifth element (which has highest probability) came out first. It should be most of the time.
        freq4 = (array(first) == 4).sum()/float(n)
        assert freq4 > 0.8, "Error in ordering elements in probsample_noreplace"
        
#        probs=array([1, 1, 1, 1, 1, 1, 0.001, 1, 1, 1])
#        probsum = float(probs.sum())
#        last=[]
#        for i in range(n):
#            sample = probsample_noreplace(arange(10), 9, prob_array=probs/probsum, return_index=False)
#            # keep the last element sampled if seventh element sampled
#            if (sample == 6).sum() > 0:
#                print sample
#                last.append(sample[8])
#        # How many times the seventh element (which has lowest probability) came out last. It should be most of the time.
#        alast = array(last)
#        freq6 = 1
#        if alast.size > 0:
#            freq6 = (array(last) == 6).sum()/float(alast.size)
#        print last
#        print freq6
#        assert freq6 > 0.8, "Error in ordering elements in probsample_noreplace"
        
    def test_prob2dsample(self):
        start_time = time.time()
        sample = prob2dsample(self.all, self.sample_size, self.prob, return_index=True)
        logger.log_status("prob2dsample (%s, %s) items array in " % self.sample_size + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.shape, self.sample_size, msg ="sample size not equal to sample size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"
        assert all(not_equal(self.prob[sample], 0.0)), "elements with zero weight in the sample"
        for i in range(sample.shape[0]):
            assert not sometrue(find_duplicates(sample[i,:])), "there are duplicates in samples at row %s" % i

    def test_sample_choice(self):
        prob = array([[0.25, 0.25, 0.25, 0.25],
                                 [0, 0, 1, 0],
                                 [0.99, 0, 0.001, 0.009]])
        start_time = time.time()
        sample = sample_choice(prob)
        logger.log_status("sample_choice from (%s, %s) items array in " % prob.shape + str(time.time() - start_time) + " sec")
        self.assertEqual(sample[0].size, prob.shape[0], msg ="sample size not equal to sample size parameter")
        self.assertEqual(prob[sample].size, prob.shape[0], msg ="sample size not equal to sample size parameter")
        assert 0 <= sample[1].min() <= prob.shape[1]-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample[1].max() <= prob.shape[1]-1, "sampled elements not in between min and max of source array"
        assert all(not_equal(prob[sample], 0.0)), "elements with zero weight in the sample"

    def test_stratifiedsample(self):
        #TODO write unittest for stratifiedsample
        pass

if __name__ == "__main__":
    opus_unittest.main()
