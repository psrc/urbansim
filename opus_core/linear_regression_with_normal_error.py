# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import sqrt, resize
from numpy.random import normal
from opus_core.linear_regression import linear_regression


class linear_regression_with_normal_error(linear_regression):
    """    Class for computing linear regression with adding normally distributed random error.
    """
    def run(self, data, coefficients, resources=None):
        """
        Return a 1D array of outcomes of linear regression (1 outcome per observation) + random error ~ N(m, sd).
        By default, m=0, sd=1. These values can be changed by resources entries 'linear_regression_error_mean' and 
        'linear_regression_error_variance'. These entries can be either a single value or an array of size data.shape[0].
        'coefficients' is a 1D array.
        'data' is a 2D numpy array of the actual data (nobservations x ncoefficients),
        """
        linear_combination = linear_regression.run(self, data, coefficients, resources=resources)
        m = 0
        sd = 1
        if resources is not None:
            m = resources.get('linear_regression_error_mean', 0)
            sd = sqrt(resources.get('linear_regression_error_variance', 1))
        return linear_combination + resize(normal(m, sd), (data.shape[0],))

from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from numpy import array

class LinearRegressionWithNormalErrorTests(StochasticTestCase):
    def setUp(self):
        self.data = array([[3,5,6,5],[2,1,0,0],[7,2,3,5]])
        self.coefficients = array([2.5, 1.2, 4, 9])
        self.known_means = array([ 82.5,   6.2,  76.9])
        self.resources = None
        def run():
            return linear_regression_with_normal_error().run(self.data, self.coefficients, resources=self.resources)
        self.func = run
        
    def test_linear_regression_with_default_normal_error(self):
        self.chi_square_test_with_known_mean(self.func, self.known_means, array(3*[1.0]), 100, significance_level=0.0001)

    def test_linear_regression_with_normal_error_single_values(self):
        """ means and variances of the error term are the same for all dataset values.
        """
        m = 20
        var = 10
        self.resources = {'linear_regression_error_mean': m, 'linear_regression_error_variance': var}
        self.chi_square_test_with_known_mean(self.func, self.known_means+m, array(3*[var]), 100, significance_level=0.0001)
        
    def test_linear_regression_with_normal_error_multiple_values(self):
        """ means and variances of the error term are differents for each dataset member.
        """
        m = array([20, 30, 40])
        var = array([10, 1, 100])
        self.resources = {'linear_regression_error_mean': m, 'linear_regression_error_variance': var}
        self.chi_square_test_with_known_mean(self.func, self.known_means+m, var, 100, significance_level=0.0001)
        
if __name__ == '__main__':
    opus_unittest.main()
