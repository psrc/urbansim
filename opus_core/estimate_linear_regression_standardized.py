# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.estimate_linear_regression import estimate_linear_regression
from opus_core.logger import logger
from opus_core import ndimage

class estimate_linear_regression_standardized(estimate_linear_regression):
    """
    Class for estimating linear regression using standardized predictors, 
    using (X-mean(X))/(scale*sd(X)) where scale can be set in resources['scale_for_data_standardization']
    and defaults to 2.
    CAUTION: Do not save estimation results when using this module, as the simulation does not standardize data.
    Use this only for exploratory analysis. For example, the method model_explorer.plot_coefficients can be useful
    in connection with this module.
    """

    def run(self, data, regression=None, resources=None):
        if data.ndim < 2:
            raise Exception("Argument 'data' must be a 2D numpy array.")
        
        scale = resources.get("scale_for_data_standardization", 2)
        for i in range(data.shape[1]):
            data[:,i] = (data[:,i] - data[:,i].mean())/(scale*ndimage.standard_deviation(data[:,i]))
        logger.log_status('Data has been standardized using (X-mean(X))/(%s*sd(X))' % scale)
        return estimate_linear_regression.run(self, data, regression=regression, resources=resources)
        