#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.resources import Resources
from numpy import zeros, float32, arange, reshape, array
from opus_core.misc import quantile, write_table_to_text_file, write_to_text_file, corr
from opus_core.linear_utilities import linear_utilities
from opus_core.logger import logger

class linear_utilities_diagnose(linear_utilities):
    """    Class for diagnosing linear utilities.
    """
    def run(self, data, coefficients, resources=None):
        """
        Like linear_utilities, but in addition it runs linear utilities for
        modified data and stores utilities when each variable is set to its 5%, 95% quantiles,
        keeping the other variables at their median. Last row in the resulting file is the difference in
        utilities between these two.
        The file name can be passed in resources - entry 'utilities_diagnose_file'.
        """
        if data.ndim < 3:
            raise StandardError, "Argument 'data' must be a 3D numpy array."

        if not isinstance(resources, Resources):
            resources= Resources(resources)
        nobs, neqs, nvar = data.shape
        medians = zeros(nvar, dtype=float32)
        quant = zeros((2,nvar), dtype=float32)
        data_with_medians = array(data[0,:,:])
        for ivar in range(nvar): # compute medain and quantiles for each variable
            medians[ivar], quant[0,ivar], quant[1,ivar] = quantile(data[:,:,ivar].ravel(), array([0.5, 0.05, 0.95]))
            data_with_medians[:,ivar] = medians[ivar]


        file_name = resources.get("utilities_diagnose_file", "util")
        if resources.get("submodel", None) is not None:
            file_name = "%s_submodel_%s" % (file_name, resources.get("submodel", 1))
        diagnose_utilities = zeros((3, nvar), dtype=float32)
        argcor = ()
        for ivar in range(nvar): # iterate over variables
            for iquant in [0,1]: # 0 for 5% quantile, 1 for 95% quantile
                mod_data = array(data_with_medians).reshape(1,neqs, nvar) # copy original data
                mod_data[0,:,ivar] = quant[iquant, ivar]
                utility = linear_utilities.run(self, mod_data, coefficients, resources)
                diagnose_utilities[iquant, ivar] = utility[0,0]
            argcor = argcor + (data[:,:,ivar].ravel(),)
        diagnose_utilities[2,:] = diagnose_utilities[1,:] - diagnose_utilities[0,:]
        coef_names = resources.get("coefficient_names", map(lambda x: 'x%s' % x, arange(nvar)+1))
        write_to_text_file(file_name, coef_names, delimiter=' ')
        write_table_to_text_file( file_name, diagnose_utilities, mode='ab')
        logger.log_status("Diagnosed utilities written into %s." % file_name)
        # compute and store correlation
        correlation = corr(*argcor)
        file_name = resources.get("correlation_diagnose_file", "correlation")
        if resources.get("submodel", None) is not None:
            file_name = "%s_submodel_%s" % (file_name, resources.get("submodel", 1))
        write_to_text_file(file_name, coef_names, delimiter=' ')
        write_table_to_text_file( file_name, correlation, mode='ab')
        logger.log_status("Data correlation written into %s." % file_name)
        return linear_utilities.run(self, data, coefficients, resources)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
class LinearUtilitiesTests(opus_unittest.OpusTestCase):
    def test_linear_utilities_1D_coef(self):
        # It is switched off in order not to create any files
        data = array([[[3,5,6,5],[2,1,0,0],[7,2,3,5]],[[5,1,5,2],[4,7,9,2],[7,2,3,5]]])
        coefficients = array([2.5, 1.2, 4, 9])
        utilities = linear_utilities_diagnose().run(data, coefficients)
        shoud_be = array([[ 82.5,   6.2,  76.9], [ 51.7,  72.4,  76.9]])
        self.assertEqual(ma.allclose(utilities, shoud_be, rtol=1e-05),
                             True, msg = "Error in test_linear_utilities_1D_coef")


if __name__ == '__main__':
    opus_unittest.main()