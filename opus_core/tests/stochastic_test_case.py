# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.tests import opus_unittest

from time import localtime, strftime

from numpy import zeros, sqrt, log, float32, sum, array, arange, reshape
from opus_core.ndimage import variance
from numpy import ma

from opus_core.variables.variable import ln
from opus_core.logger import logger
from opus_core.third_party.pstat import chisqprob
from opus_core.misc import get_host_name, try_transformation
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.tests.utils.opus_test_runner import get_test_method_name

class StochasticTestCase(opus_unittest.OpusTestCase):
    """A way to do statistically-grounded testing of stochastic system.
    """
    def run_stochastic_test(self, file_path, function, expected_results,
                            number_of_iterations, significance_level=0.01, type="poisson", transformation=None,
                            expected_to_fail=False, number_of_tries=5):
        """
        For each test, run the given function for the specified number_of_iterations.
        Uses different test statistics to determine whether the produced results are
        within the specified significance_level of the expected_results.
        Finally, since the stochastic test will fail every once in a while, run the whole
        test up to number_of_tries times, until either it succeeds or it fails too many times.
        """
        self.file_path = file_path
        self.type = type
        self.expected_to_fail = expected_to_fail
        for i in range(number_of_tries):
            if type == "normal":
                (passed, msg) = self._run_stochastic_test_normal(function, expected_results,
                            number_of_iterations, significance_level, transformation)
            elif type == "poisson":
                (passed, msg) = self._run_stochastic_test_poisson(function, expected_results,
                            number_of_iterations, significance_level, transformation)
            elif type == "pearson":
                (passed, msg) = self._run_stochastic_test_pearson(function, expected_results,
                            number_of_iterations, significance_level, transformation)
            else:
                raise TypeError, "Unknown type of stochastic test."
            if passed:
                return
        # failed too many times -- show the last message
        self.fail(msg)

    def _run_stochastic_test_normal(self, function, expected_results,
                            number_of_iterations, significance_level=0.01, transformation="sqrt"):
        K, LRTS, prob = self.compute_stochastic_test_normal(function, expected_results,
                            number_of_iterations, significance_level, transformation)
        logger.log_status("Stochastic Test Normal: LRTS=" + str(LRTS) + ", df=", str(K), " p=" + str(prob))
        return (prob >= significance_level, "prob=%f < significance level of %f" % (prob, significance_level))

    def compute_stochastic_test_normal(self, function, expected_results,
                            number_of_iterations, significance_level=0.01, transformation="sqrt"):
        K = expected_results.size
        sum_y = zeros(K, dtype=float32)
        x_kr = zeros((number_of_iterations, K), dtype=float32)
        texpected_results = try_transformation(expected_results, transformation)
        for i in range(number_of_iterations):
            y_r = function()
            x_kr[i,:] = try_transformation(y_r, transformation)
            sum_y = sum_y + x_kr[i,:]
        muest = sum_y/float(number_of_iterations)
        sigma_1 = ((x_kr - muest)**2.0).sum()/float(number_of_iterations*K)
        self.variance = variance(x_kr, labels=reshape(array(number_of_iterations*range(1,K+1)),
                                                    (number_of_iterations,K)),
                                 index=arange(K)+1)
        sigma_0 = ((x_kr - texpected_results)**2.0).sum()/float(number_of_iterations*K)
        LRTS = number_of_iterations*K * log(sigma_0/sigma_1)
        prob = chisqprob(LRTS, K)
        return (K, LRTS, prob)

    def _run_stochastic_test_poisson(self, function, expected_results,
                            number_of_iterations, significance_level=0.01, transformation=None):
        """
        Run the given function for the specified number_of_iterations.
        Uses Bayesian statistics to determine whether the produced results are
        within the specified significance_level of the expected_results.
        """
        K = expected_results.size
        sum_y = zeros(K, dtype=float32)
        x_kr = zeros((number_of_iterations, K), dtype=float32)
        for i in range(number_of_iterations):
            y_r = function()
            x_kr[i,:] = try_transformation(y_r, transformation)
            sum_y = sum_y + x_kr[i,:]
        lambdak = sum_y/float(number_of_iterations)
        lambdanull = try_transformation(expected_results.astype(float32), transformation)
#        print lambdak
#        print lambdanull
        sumxk = sum(x_kr, axis=0)
        LRTS = 2.0* ((number_of_iterations*(lambdanull-lambdak).sum()) + (ln(lambdak/ma.masked_where(lambdanull==0, lambdanull))*sumxk).sum())
        prob = chisqprob(LRTS, K)
        #print LRTS, prob
        logger.log_status("Stochastic Test Poisson: LRTS=" + str(LRTS) + ", df=", str(K), ", p=" + str(prob))
        return (prob >= significance_level, "prob=%f < significance level of %f" % (prob, significance_level))

    def _run_stochastic_test_pearson(self, function, expected_results,
                            number_of_iterations, significance_level=0.01, transformation=None):
        K = expected_results.size
        x_kr = zeros((number_of_iterations, K), dtype=float32)
        for i in range(number_of_iterations):
            x_kr[i,:]= function()
        mue = expected_results.astype(float32)
        pearson = 0.0
        for k in range(K):
            pearson = pearson + (((x_kr[:,k] - mue[k])**2.0)/mue[k]).sum()
        prob = chisqprob(pearson, K*number_of_iterations)
        #print pearson, prob
        logger.log_status("Stochastic Test: Pearson Chi^2=" + str(pearson) + ", df=",
                           str(K*number_of_iterations),", p=" + str(prob))
        return (prob >= significance_level, "prob=%f < significance level of %f" % (prob, significance_level))

    def chi_square_test_with_known_mean(self, function, mean, variance, number_of_iterations, significance_level=0.01, number_of_tries=5):
        """For each test, run a two-sided Chi^2 test for sigma = sigma_0 vs. sigma != sigma_0, if means are known.
        'mean' and 'variance' are arrays whose length must correspond to the array that the given function produces.
        Since the stochastic test will fail every once in a while, run the whole
        test up to number_of_tries times, until either it succeeds or it fails too many times.
        """
        for i in range(number_of_tries):
            K = mean.size
            x = zeros((number_of_iterations, K), dtype=float32)
            for i in range(number_of_iterations):
                x[i,:]= function()
            stat = (((x - mean)**2.0)/variance).sum()
            prob = chisqprob(stat, K*number_of_iterations)
            logger.log_status("Stochastic Test: Chi^2 test statistic = " + str(stat) + ", df=",
                               str(K*number_of_iterations),", p=" + str(prob))
            if (prob >= significance_level/2.0) and (prob <= (1-significance_level/2.0)):
                # test succeeded -- jump out of the method
                return
        # test failed more than number_of_tries times
        self.fail(msg="prob=%f is not in [%f,%f]" % (prob, significance_level/2.0, 1-significance_level/2.0))
        
 
class TestStochasticTestCase(opus_unittest.OpusTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    ### TODO:
    def test_run_stochastic_test_normal(self):
        pass

    ### TODO:
    def test_run_stochastic_test_poisson(self):
        pass

    ### TODO:
    def test_run_stochastic_test_pearson(self):
        pass


### TODO:
class StochasticTestCaseTestCase(StochasticTestCase):
    pass


if __name__ == '__main__':
    opus_unittest.main()
