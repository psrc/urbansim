# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.estimation_procedure import EstimationProcedure
from numpy import array, zeros, float32, dot, transpose, concatenate
from numpy import ones, sqrt, diagonal, log
from opus_core.logger import logger
from numpy.linalg import inv, det
from opus_core.misc import check_dimensions

class estimate_linear_regression(EstimationProcedure):
    """    Class for estimating linear regression.
    """
    def run(self, data, regression=None, resources=None):

        """
        Expects an entry 'outcome' in resources that provides the values of the dependent variable.
        'data' is a 2D numpy array of the acctual data (nobservations x ncoefficients),
            it can be created by Dataset.create_regression_data_for_estimation(...).
        'regression' is an instance of the Regression class (it is not used in this module).
        Return a dictionary with results.
        """
        if data.ndim < 2:
            raise StandardError, "Argument 'data' must be a 2D numpy array."
        tags = ["estimate", "result"]
        vl = 2
        nobs = data.shape[0]
        nvar = data.shape[1]
        constant_position = resources.get("constant_position",  array([], dtype='int32')) #position for intercept
        if constant_position.size <=0:
            constant_position=-1
            nvalues = nvar
            X = data
        else:
            constant_position=constant_position[0]
            nvalues = nvar+1
            X = concatenate((ones((nobs,1)), data), axis=1)

        beta = zeros(nvalues).astype(float32)
        outcome = resources["outcome"]

        tX = transpose(X)
        try:
            Csquared = inv(dot(tX,X))
        except:
            logger.log_warning("Estimation led to singular matrix. No results.",
                               tags=tags, verbosity_level=vl)
            return {}
        if det(Csquared) < 1e-20:
            logger.log_warning("Estimation may led to singularities. Results may be not correct.")
        tmp = dot(Csquared, tX)
        estimates = dot(tmp,outcome)
        Residuals = outcome - dot(X, estimates)
        if nobs-nvalues <= 0:
            logger.log_warning("Less observations than variables. No results.",
                                tags=tags, verbosity_level=vl)
            return {}
        s2 = dot(transpose(Residuals), Residuals)/float(nobs-nvalues)
        standard_errors = sqrt(diagonal(s2*Csquared))
        values = zeros((nvalues,), dtype=float32)
        se = zeros((nvalues,), dtype=float32)
        toutcome = transpose(outcome)
        ybar = outcome.sum()/float(nobs)
        ysquared = ybar*ybar
        nysquared = nobs * ysquared
        SSR = dot(dot(dot(toutcome, X), tmp),outcome) - nysquared
        SST = dot(toutcome, outcome) - nysquared
        Rsquared = SSR/SST
        Rsquared_adj = 1.0- (nobs-1)/float(nobs-nvalues)*(1.0-Rsquared)

        if constant_position>=0:
            values[constant_position] = estimates[0]
            se[constant_position] = standard_errors[0]
            start = 1
        else:
            start=0

        j=0
        for i in range(start,nvar+start):
            if j == constant_position:
                j+=1
            values[j] = estimates[i]
            se[j] = standard_errors[i]
            j+=1

        tvalues = values/se
        result = {"estimators":values, "standard_errors":se,
                   "other_measures":{"t_statistic":tvalues},
                    "other_info":{"R-Squared":Rsquared,
            "Adjusted R-Squared":Rsquared_adj}}

        names = resources.get("coefficient_names",  nvar*[])
        logger.log_status("R-Squared:            ", Rsquared, tags=tags, verbosity_level=vl)
        logger.log_status("Adjusted R-Squared:   ", Rsquared_adj, tags=tags, verbosity_level=vl)
        logger.log_status('Suggested |t-value| > ', sqrt(log(nobs)))
        logger.log_status("-----------------------------------------------", tags=tags, verbosity_level=vl)
        logger.log_status("Coeff_names\testimate\tSE\tt-values", tags=tags, verbosity_level=vl)
        if constant_position>=0:
            logger.log_status("%10s\t%8g\t%8g\t%8g" % ("constant", estimates[0], standard_errors[0],
                                    estimates[0]/standard_errors[0]), tags=tags, verbosity_level=vl)
        for i in range(nvar):
            logger.log_status("%10s\t%8g\t%8g\t%8g" % (names[i],estimates[i+start],standard_errors[i+start],
                                    estimates[i+start]/standard_errors[i+start]), tags=tags, verbosity_level=vl)
        logger.log_status("===============================================", tags=tags, verbosity_level=vl)
        logger.log_status(tags=tags, verbosity_level=vl)

        return result

