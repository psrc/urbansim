# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import sum
from opus_core.misc import check_dimensions
from opus_core.utilities import Utilities
from numpy.core.umath_tests import inner1d

class linear_utilities(Utilities):
    """    Class for computing linear utilities.
    """
    def run(self, data, coefficients, resources=None):
        """
        Return a 2D array of utilities (nobservations x nequations).
        'coefficients' is a 2D array of coefficients (nequations x ncoefficients).
        'data' is a 3D numpy array of the actual data (nobservations x nequations x ncoefficients),
            it can be created by InteractionDataset.create_logit_data(...).
        """
        if data.ndim < 3:
            raise StandardError, "Argument 'data' must be a 3D numpy array."

        if coefficients.ndim > 1:
            if not check_dimensions(data[0,:,:], coefficients):
                raise StandardError, "Mismatch in dimensions of data and coefficients."

        utility = inner1d(data, coefficients)
        return utility

from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
class LinearUtilitiesTests(opus_unittest.OpusTestCase):
    def test_linear_utilities_1D_coef(self):
        data = array([[[3,5,6,5],[2,1,0,0],[7,2,3,5]],[[5,1,5,2],[4,7,9,2],[7,2,3,5]]])
        coefficients = array([2.5, 1.2, 4, 9])
        utilities = linear_utilities().run(data, coefficients)
        shoud_be = array([[ 82.5,   6.2,  76.9], [ 51.7,  72.4,  76.9]])
        self.assertEqual(ma.allclose(utilities, shoud_be, rtol=1e-05),
                             True, msg = "Error in test_linear_utilities_1D_coef")

    def test_linear_utilities_2D_coef(self):
        data = array([[[3,5,6,5],[2,1,0,0],[7,2,3,5]],[[5,1,5,2],[4,7,9,2],[7,2,3,5]]])
        coefficients = array([[2.5, 1.2, 4, 9], [1, 2, 3, 4], [0, 3, 2.3, 4]])
        utilities = linear_utilities().run(data, coefficients)
        shoud_be = array([[ 82.5,   4,  32.9], [ 51.7,  53,  32.9]])
        self.assertEqual(ma.allclose(utilities, shoud_be, rtol=1e-05),
                             True, msg = "Error in test_linear_utilities_2D_coef")

if __name__ == '__main__':
    opus_unittest.main()
