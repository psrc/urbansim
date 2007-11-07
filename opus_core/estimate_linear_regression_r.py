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

from opus_core.estimation_procedure import EstimationProcedure
from rpy import r, set_default_mode, NO_CONVERSION, BASIC_CONVERSION
from numpy import array, zeros, float32, swapaxes
from numpy import sqrt, log
from opus_core.logger import logger
from opus_core.misc import check_dimensions

class estimate_linear_regression_r(EstimationProcedure):
    """    Class for estimating linear regression using the R function lm (rpy required).        
    """
    #def run(self, data, coefficients, resources=None):
    def run(self, data, regression=None, resources=None):
        """
        Expects an entry 'outcome' in resources that provides the values of the dependent variable.
        'coefficients' is of type "SpecifiedCoefficientsFor1Submodel". 
        'data' is a 2D numpy array of the acctual data (nobservations x ncoefficients), 
            it can be created by Dataset.create_regression_data_for_estimation(...).
        Return the modified coefficients.
        """
        if data.ndim < 2:
            raise StandardError, "Argument 'data' must be a 2D numpy array."
        tags = ["estimate", "result"]
        vl = 2
            
        #beta = coefficients.get_coefficient_values()[0,:] # we are interested only in one equation
        nobs = data.shape[0]
        nvar = data.shape[1]
        #constant_position = coefficients.get_constants_positions()
        constant_position = resources.get("constant_position",  array([], dtype='int32')) #position for intercept
        if constant_position.size <=0: #position for intercept
            constant_position=-1
            nvalues = nvar
        else:
            constant_position=constant_position[0]
            nvalues = nvar+1

        beta = zeros(nvalues).astype(float32)

        if beta.size <> nvalues:
            raise StandardError, "Mismatch in dimensions of 'data' and 'coefficients.beta'."
            
        #coef_names = coefficients.get_coefficient_names_without_constant()
        coef_names = resources.get("coefficient_names",  nvar*[])
        #rnames = array(map(lambda x: "x."+ str(x), range(1,nvar+1)))
        #coef_names_array = swapaxes(array([coef_names[0,:], rnames]),1,0)
        #logger.log_status(coef_names_array)
        # Rpy doesn't like float32, but is okay with float64
        outcome = resources["outcome"].astype("float64")
        set_default_mode(NO_CONVERSION)
        
        # Rpy doesn't like float32, but is okay with float64
        data_for_r = data.astype("float64")
        d = r.data_frame(x=data_for_r,y=outcome)
        expression = "y ~ x.1"
        for i in range(2,nvar+1):
            expression=expression+" + x."+str(i)
        model = r(expression)
        fit = r.lm(model, data=d)
        
        # Begin, for AIC
        # WARNING: Make sure this code appears just after the call to r.lm.
        #          If it appears after the call to r.summary, the call to
        #          r.AIC will crash
        set_default_mode(BASIC_CONVERSION)
        aic = r.AIC(fit)
        set_default_mode(NO_CONVERSION)
        # End, for AIC
        
        summary = r.summary(fit)
        summary[0]=expression
        
        #r.print_(summary)
        set_default_mode(BASIC_CONVERSION)
        new_coef = r.coefficients(fit)
        values = zeros((nvalues,), dtype=float32)
        se = zeros((nvalues,), dtype=float32)
        if constant_position>=0:
            values[constant_position] = new_coef["(Intercept)"]
            start = 1
            try:
                se[constant_position] = summary[3]["coefficients"][0,1]
            except:
                pass
        else:
            start = 0
        j=0
        for i in range(1,nvar+1):
            if j == constant_position:
                j+=1
            values[j] = new_coef["x."+str(i)]
            try:
                se[j] = summary[3]["coefficients"][i,1]
            except:
                pass
            j+=1
        #coefficients.set_coefficient_values(values)
        #coefficients.set_standard_errors(se)
        #coefficients.set_measure("t-statistic", values/se)
        #return coefficients
        
        # r.summary(fit)['coefficients'] is a 2D array of the following structure:
        # [ [estimate, standard error, t-value, p-value], ...]
        # To get an array of the estimates for all the variables, slice off the first column:
        estimates = r.summary(fit)['coefficients'][:,0]
        # To get an array of the standard errors for all of the variables, slice off the second column:
        standard_errors = r.summary(fit)['coefficients'][:,1]
        
        Rsquared = r.summary(fit)['r.squared']
        Rsquared_adj = r.summary(fit)['adj.r.squared']
        
        tvalues = values/se
        result = {"estimators":values, "standard_errors":se,
                   "other_measures":{"t_statistic":tvalues},
                    "other_info":{"R-Squared":Rsquared,
            "Adjusted R-Squared":Rsquared_adj}}

        logger.log_status("Akaike's Information Criterion (AIC): ", str(aic), tags=tags, verbosity=vl)

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
        

        
