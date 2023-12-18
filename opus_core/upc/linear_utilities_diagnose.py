# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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
            raise Exception("Argument 'data' must be a 3D numpy array.")

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
        coef_names = resources.get("coefficient_names", ['x%s' % x for x in arange(nvar)+1])
        write_to_text_file(file_name, coef_names, delimiter=' ')
        write_table_to_text_file( file_name, diagnose_utilities, mode='ab')
        logger.log_status("Diagnosed utilities written into %s." % file_name)
        return linear_utilities.run(self, data, coefficients, resources)
