# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.estimation_procedure import EstimationProcedure
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri # this turns on an automatic conversion from numpy to rpy2 objects
from numpy import array, zeros, float32, swapaxes, asarray, arange, asmatrix
from numpy import sqrt, log
from opus_core.logger import logger
from opus_core.misc import check_dimensions

class estimate_linear_regression_r(EstimationProcedure):
    """    Class for estimating linear regression using the R function lm (rpy2 required).        
    """
    def run(self, data, regression=None, resources=None):
        """
        Expects an entry 'outcome' in resources that provides the values of the dependent variable.
        'coefficients' is of type "SpecifiedCoefficientsFor1Submodel". 
        'data' is a 2D numpy array of the acctual data (nobservations x ncoefficients), 
            it can be created by Dataset.create_regression_data_for_estimation(...).
        Return the modified coefficients.
        """
        r = robjects.r
        if data.ndim < 2:
            raise StandardError, "Argument 'data' must be a 2D numpy array."
        tags = ["estimate", "result"]
        vl = 2
            
        nobs = data.shape[0]
        nvar = data.shape[1]
        constant_position = resources.get("constant_position",  array([], dtype='int32')) #position for intercept
        if constant_position.size <= 0: #position for intercept
            constant_position=-1
            # Used for printing results below
            start = 0
        else:
            constant_position=constant_position[0]     
            # Used for printing results below
            start = 1

        # R doesn't like "x.i" notation when there's a single independent variable
        if nvar < 2:
            expression = "y ~ x"
        else:
            expression = "y ~ x.1"

        d = robjects.DataFrame({'x': data, 'y': resources["outcome"]})
        
        for i in range(2,nvar+1):
            expression=expression+" + x."+str(i)
        model = r(expression)
        fit = r.lm(model, data=d)
        aic = r.AIC(fit)
        s = r.summary(fit)
                
        # r.summary(fit)['coefficients'] is a 2D array of the following structure:
        # [ [estimate, standard error, t-value, p-value], ...]
        # To get an array of the estimates for all the variables, slice off the first column:
        
        coefidx = arange(len(list(s)))[asarray(r.names(s)) == "coefficients"]
        estimates = asmatrix(list(s)[coefidx])[:,0]
        if estimates.size < nvar+1:
            logger.log_warning('There was an error in estimating the model. Possibly singularities found.')
            return {"estimators":zeros(nvar+1), "standard_errors":zeros(nvar+1)}
 
        # To get an array of the standard errors for all of the variables, slice off the second column:
        standard_errors = asmatrix(list(s)[coefidx])[:,1]
        
        rsqidx = arange(len(list(s)))[asarray(r.names(s)) == "r.squared"]
        Rsquared = asarray(list(s)[rsqidx])[0]
        rsqaidx = arange(len(list(s)))[asarray(r.names(s)) == "adj.r.squared"]
        Rsquared_adj = asarray(list(s)[rsqaidx])[0]
        
        tvalues = estimates/standard_errors
        result = {"estimators":estimates, "standard_errors":standard_errors,
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
                                    tvalues[0]), tags=tags, verbosity_level=vl)
        for i in range(nvar):
            logger.log_status("%10s\t%8g\t%8g\t%8g" % (names[i],estimates[i+start],standard_errors[i+start],
                                    tvalues[i+start]), tags=tags, verbosity_level=vl)
        logger.log_status("===============================================", tags=tags, verbosity_level=vl)
        logger.log_status(tags=tags, verbosity_level=vl)
        
        return result
        

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from numpy import array, resize


class Tests(opus_unittest.OpusTestCase):
    """ Unit tests for opus_core.estimate_linear_regression_r
    """
    def skip_test_estimation_one_var(self):
        """ Test a regression estimation for a model with one independent variable
        """
        
        # First, use scipy to get reference values to compare the results of our
        # R-based regression to.
        #print "using scipy to calculate reference regression..."
        # Example regression from: http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/lin_reg/
        from scipy import stats
        x = [5.05, 6.75, 3.21, 2.66]
        y = [1.65, 26.5, -5.93, 7.96]
        gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        r_squared = r_value**2
        #print "Gradient and intercept", gradient, intercept
        ##Gradient and intercept 5.3935773612 -16.2811279931
        #print "R-squared", r_squared
        ##R-squared 0.524806275136
        #print "p-value", p_value
        ##p-value 0.275564857882
        
        # Next, setup the call to estimate_linear_regression_r.run(...)
        # Need to call run method on estimate_linear_regression_r, whose prototype is: 
        #   def run(self, data, regression=None, resources=None):
        #   regresion is not used by the run method
        #   things I need to store in resources:
        #     constant_position = resources.get("constant_position",  array([], dtype='int32')) #position for intercept
        #     coef_names = resources.get("coefficient_names",  nvar*[])
        #     outcome = resources["outcome"].astype("float64")
        
        # Create resources
        coeff = array(['EX'])
        resources = Resources()
        # No constant
        resources.add("constant_position", array([], dtype='int32'))
        resources.add("coefficient_names", coeff)
        resources.add("outcome", array(y))
        
        #data = array([x, y])
        data = resize(array([x]), (len(x), 1))
        
        # run RPy-based regression
        estimateR = estimate_linear_regression_r()
        result = estimateR.run(data, resources=resources)
        #print "results from RPy-base estimation: " + str(result)
    
        # Finally, compare the scipy-based regression to the R-based regression
        # Compare estimate of the independent 
        self.assertEqual(round(intercept, 4), round(result['estimators'][0], 4))
        # Compare the R-Squared
        self.assertEqual(round(r_squared, 6), round(result['other_info']['R-Squared'], 6))
    
if __name__=='__main__':
    try: import wingdbstub
    except: pass

    opus_unittest.main()
