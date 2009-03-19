# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
from rpy import r, set_default_mode, NO_CONVERSION
from numpy import zeros, float32, array
from opus_core.estimation_procedure import EstimationProcedure
from opus_core.logger import logger

class bma_for_linear_regression_r(EstimationProcedure):
    """    Class for variable selection in a linear regression using R package BMA.
    It prints out results computed by the R function bic.glm and plots an image of the results.
    You need to have installed R, rpy and the R package BMA.
    """
    def run(self, data, regression, resources=None):
        """
        The method prints out summary of the BMA procedure and creates an imageplot.
        If resources has an entry 'bma_imageplot_filename', the imageplot is sent to this file as pdf.
        The method does not return any useful results - it is a tool for variable selection.
        Once you selected your variables, use estimate_linear_regression for further usage of the coefficients. 
        
        Expects an entry 'outcome' in resources that provides the values of the dependent variable.
        'data' is a 2D numpy array of the actual data (nobservations x ncoefficients),
            it can be created by Dataset.create_regression_data_for_estimation(...).
        'regression' is an instance of a regression class.
        """
        if data.ndim < 2:
            raise StandardError, "Argument 'data' must be a 2D numpy array."

        nobs = data.shape[0]
        nvar = data.shape[1]
        constant_position = resources.get("constant_position",  array([], dtype='int32')) #position for intercept

        if constant_position.size == 0: #position for intercept
            constant_position=-1
            nvalues = nvar
        else:
            constant_position=constant_position[0]
            nvalues = nvar+1

        beta = zeros(nvalues).astype(float32)

        coef_names = resources.get("coefficient_names",  nvar*[])
        outcome = resources["outcome"].astype("float64")
        set_default_mode(NO_CONVERSION)
        r.library("BMA")
        data_for_r = data.astype("float64")
        d = r.data_frame(r.matrix(data_for_r, ncol=nvar, dimnames=[[],coef_names]))
        try:
            fit = r.bic_glm(x=d, y=outcome, glm_family="gaussian", strict=1)
            fit[20] = '' # to have less output in the summary
            r.summary(fit)
            filename = resources.get('bma_imageplot_filename', None)
            if filename is not None:
                r.pdf(file=filename)
                r.imageplot_bma(fit)
                r.dev_off()
            else:
                r.imageplot_bma(fit)
        except:
            logger.log_warning("Error in BMA procedure.")
        return {}

