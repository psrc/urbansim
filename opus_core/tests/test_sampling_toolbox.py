# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.sampling_toolbox import sample_replace
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.sampling_toolbox import probsample_replace
from opus_core.sampling_toolbox import probsample_noreplace
from opus_core.sampling_toolbox import find_duplicates
from opus_core.sampling_toolbox import prob2dsample
from opus_core.sampling_toolbox import sample_choice
from opus_core.tests import opus_unittest
import time
from numpy import array
from numpy import sometrue, alltrue, not_equal, ndarray
from numpy import float32, all
from numpy.random import randint
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
        sample = sample_replace(self.all, self.size, return_indices=True)
        logger.log_status("sample_replace %s from %s items array in " % (self.size,self.n) + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.size, self.size, msg ="sample size not equal to size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"

    def test_sample_noreplace(self):
        start_time = time.time()
        sample = sample_noreplace(self.all, self.size, return_indices=True)
        logger.log_status("sample_noreplace %s from %s items array in " % (self.size,self.n) + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.size, self.size, msg ="sample size not equal to size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"
        assert not sometrue(find_duplicates(sample)), "there are duplicates in samples"

    def test_probsample_replace(self):
        start_time = time.time()
        sample = probsample_replace(self.all, self.size, self.prob, return_indices=True)
        logger.log_status("probsample_replace %s from %s items array in " % (self.size,self.n) + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.size, self.size, msg ="sample size not equal to size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"
        assert alltrue(not_equal(self.prob[sample], 0.0)), "elements with zero weight in the sample"

    def test_probsample_noreplace(self):
        start_time = time.time()
        sample = probsample_noreplace(self.all, self.size, self.prob, return_indices=True)
        logger.log_status("probsample_noreplace %s from %s items array in " % (self.size,self.n) + str(time.time() - start_time) + " sec")
        self.assertEqual(sample.size, self.size, msg ="sample size not equal to size parameter")
        assert isinstance(sample, ndarray), "sample is not of type ndarray"
        assert 0 <= sample.min() <= self.n-1, "sampled elements not in between min and max of source array"
        assert 0 <= sample.max() <= self.n-1, "sampled elements not in between min and max of source array"
        assert alltrue(not_equal(self.prob[sample], 0.0)), "elements with zero weight in the sample"
        assert not sometrue(find_duplicates(sample)), "there are duplicates in samples"

    def test_prob2dsample(self):
        start_time = time.time()
        sample = prob2dsample(self.all, self.sample_size, self.prob, return_indices=True)
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

#    def test_random_seed(self):
#        RandomSeed().set_seed((7,9))
#        seed(7,9)
#        def t(min, max, j):
#            seeds = RandomSeed().get_seed()
#            seed(seeds[0], seeds[1])
#            random_seed = get_seed()
#            return (randint(min, max, j), random_seed)
#
#        j = 10
#        min, max = (1, 100)
#        my_random_seed = get_seed()
#        r1 = randint(min, max, j)
#        time.sleep(1)
#        r2, t_random_seed = t(min, max, j)
#        self.assertEqual(my_random_seed, t_random_seed, msg="random_seed set is not equal to result of get_seed()")
#        assert alltrue(equal(r1, r2))

if __name__ == "__main__":
    opus_unittest.main()
