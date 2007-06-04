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
from rpy import *
from Numeric import array as numpy_array
from numpy import zeros, float32, swapaxes
from opus_core.misc import check_dimensions

class estimate_linear_regression_r(object):
    """    Class for estimating linear regression using the R function lm (rpy required).        
    """
    def run(self, data, coefficients, resources=None):
        """
        Expects an entry 'outcome' in resources that provides the values of the dependent variable.
        'coefficients' is of type "SpecifiedCoefficientsFor1Submodel". 
        'data' is a 2D numpy array of the acctual data (nobservations x ncoefficients), 
            it can be created by Dataset.create_regression_data_for_estimation(...).
        Return the modified coefficients.
        """
        if data.ndim < 2:
            raise StandardError, "Argument 'data' must be a 2D numpy array."
            
        beta = coefficients.get_coefficient_values()[0,:] # we are interested only in one equation
        nobs = data.shape[0]
        nvar = data.shape[1]
        constant_position = coefficients.get_constants_positions()
        if constant_position.size <=0: #position for intercept
            constant_position=-1
            nvalues = nvar
        else:
            constant_position=constant_position[0]
            nvalues = nvar+1

        if beta.size <> nvalues:
            raise StandardError, "Mismatch in dimensions of 'data' and 'coefficients.beta'."
            
        coef_names = coefficients.get_coefficient_names_without_constant()
        rnames = array(map(lambda x: "x."+ str(x), range(1,nvar+1)))
        coef_names_array = swapaxes(array([coef_names[0,:], rnames]),1,0)
        logger.log_status(coef_names_array)
        outcome = resources["outcome"]
        set_default_mode(NO_CONVERSION)
        d = r.data_frame(x=numpy_array(data),y=numpy_array(outcome))
        expression = "y ~ x.1"
        for i in range(2,nvar+1):
            expression=expression+" + x."+str(i)
        model = r(expression)
        fit = r.lm(model, data=d)
        summary = r.summary(fit)
        summary[0]=expression
        r.print_(summary)
        set_default_mode(BASIC_CONVERSION)
        new_coef = r.coefficients(fit)
        values = zeros((nvalues,), dtype=float32)
        se = zeros((nvalues,), dtype=float32)
        if constant_position>=0:
            values[constant_position] = new_coef["(Intercept)"]
            try:
                se[constant_position] = summary[3]["coefficients"][0,1]
            except:
                pass
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
        coefficients.set_coefficient_values(values)
        coefficients.set_standard_errors(se)
        coefficients.set_measure("t-statistic", values/se)
        return coefficients
        
