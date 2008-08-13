#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

import os
from opus_core.tests import opus_unittest

from time import localtime, strftime

from numpy import zeros, sqrt, log, float32, sum, array, arange, reshape
from scipy.ndimage import variance
from numpy import ma

from opus_core.variables.variable import ln
from opus_core.logger import logger
from opus_core.pstat import chisqprob
from opus_core.misc import get_host_name, try_transformation
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.tests.utils.opus_test_runner import get_test_method_name

class StochasticTestCase(opus_unittest.OpusTestCase):
    """A way to do statistically-grounded testing of stochastic system.
    """
    def run_stochastic_test(self, file_path, function, expected_results,
                            number_of_iterations, significance_level=0.01, type="poisson", transformation=None,
                            log_results=True, expected_to_fail=False, number_of_tries=5):
        """
        For each test, run the given function for the specified number_of_iterations.
        Uses different test statistics to determine whether the produced results are
        within the specified significance_level of the expected_results.
        If log_results is True, and if the operating system environment variable
        MYSQLSTOCHASTICTESTLOGGER is set, log the results to the stochastic_test_case
        table in the MySQL database on the host MYSQLSTOCHASTICTESTLOGGER.  Nothing
        is logged if log_results is False or if the environment variable isn't set.
        Finally, since the stochastic test will fail every once in a while, run the whole
        test up to number_of_tries times, until either it succeeds or it fails too many times.
        """
        self.file_path = file_path
        self.type = type
        self.log_results = log_results
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


    def _log_results(self, prob, number_of_iterations, significance_level, transformation, K, LRTS=-9999):
        """If we are logging results, and if the environment variable
        MYSQLSTOCHASTICTESTLOGGER is set, record each run in a database table
        so we can track the number of successes & failures of stochastic tests.
        Record which model, which test, number_of_iterations, significance_level,
        success/failure.  Save to a new row in a database table.
        The database access is wrapped with a try/catch block, so if the hostname
        is wrong, the MySQL user name doesn't exist, or whatever, the request to
        log the results is ignored.
        """
        if not self.log_results:
            return
        if not os.environ.has_key('MYSQLSTOCHASTICTESTLOGGER'):
            return
        #
        # The DB is only used to log the results, so if we aren't doing that,
        # we don't need a connection to the DB
        #
        try:
            from MySQLdb import escape_string
        except ImportError, e:
            return

        self.file_path = escape_string(self.file_path)

        sql = """insert into test_results
        (datetime, host_name, file_path, method_name, significance_level, number_of_iterations, statistic,
        transformation, probability, success, expected_to_fail, K, LRTS)
        values (
        '%(datetime)s',
        '%(host_name)s',
        '%(file_path)s',
        '%(method_name)s',
        %(significance_level)f,
        %(number_of_iterations)d,
        '%(statistic)s',
        '%(transformation)s',
        %(probability)f,
        %(success)i,
        %(expected_to_fail)i,
        %(K)f,
        %(LRTS)f
        )""" % {
            'datetime':strftime("%Y-%m-%d %H:%M:%S", localtime()), # time.time()
            'host_name':get_host_name(),
            'file_path':self.file_path,
            'method_name': get_test_method_name(self),
            'significance_level':significance_level,
            'number_of_iterations':number_of_iterations,
            'statistic':self.type,
            'transformation':transformation,
            'probability':prob,
            'success':prob >= significance_level,
            'expected_to_fail':self.expected_to_fail,
            'K':K,
            'LRTS':LRTS,
            }
        config = DatabaseServerConfiguration(
            host_name = os.environ['MYSQLSTOCHASTICTESTLOGGER'],
            user_name = os.environ['MYSQLUSERNAME'],
            password = os.environ['MYSQLPASSWORD'],
            )
        try:
            db_server = DatabaseServer(config)
            db = db_server.get_database('stochastic_test_case')
            db.DoQuery(sql)
        except:
            pass

    def _run_stochastic_test_normal(self, function, expected_results,
                            number_of_iterations, significance_level=0.01, transformation="sqrt"):
        K, LRTS, prob = self.compute_stochastic_test_normal(function, expected_results,
                            number_of_iterations, significance_level, transformation)
        logger.log_status("Stochastic Test Normal: LRTS=" + str(LRTS) + ", df=", str(K), " p=" + str(prob))
        self._log_results(prob, number_of_iterations, significance_level, transformation, K, LRTS)
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
        self._log_results(prob, number_of_iterations, significance_level, transformation, K, LRTS)
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
        self._log_results(prob, number_of_iterations, significance_level, transformation, K)
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
