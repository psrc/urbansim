# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import sum
from opus_core.regression import Regression
from opus_core.misc import check_dimensions

class linear_regression(Regression):
    """    Class for computing linear regression.
    """
    def run(self, data, coefficients, resources=None):
        """
        Return a 1D array of outcomes of linear regression (1 outcome per observation).
        'coefficients' is a 1D array.
        'data' is a 2D numpy array of the actual data (nobservations x ncoefficients),
            it can be created by Dataset.create_regression_data(...).
        """
        if data.ndim < 2:
            raise StandardError, "Argument 'data' must be a 2D numpy array."

        beta = coefficients
        if not check_dimensions(data[0,:], beta):
            raise StandardError, "Mismatch in dimensions of 'data' and 'coefficients.beta'."

        return sum(beta*data,axis=1)

from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
class LinearRegressionTests(opus_unittest.OpusTestCase):
    def test_linear_regression(self):
        data = array([[3,5,6,5],[2,1,0,0],[7,2,3,5]])
        coefficients = array([2.5, 1.2, 4, 9])
        outcome = linear_regression().run(data, coefficients)
        shoud_be = array([ 82.5,   6.2,  76.9])
        self.assertEqual(ma.allclose(outcome, shoud_be, rtol=1e-05),
                             True, msg = "Error in test_linear_regression")

if __name__ == '__main__':
    opus_unittest.main()