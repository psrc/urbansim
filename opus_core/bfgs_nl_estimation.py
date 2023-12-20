# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.estimation_procedure import EstimationProcedure
from opus_core.logger import logger
from numpy import zeros,log,float32,reshape,diagonal,sqrt, array, ones, where, arange, exp, clip, logical_not, identity
from numpy import sort, concatenate
from opus_core.third_party.pstat import chisqprob
from opus_core.misc import get_indices_of_matched_items, ematch
from scipy.optimize import fmin_bfgs, fmin_l_bfgs_b
import time

class bfgs_nl_estimation(EstimationProcedure):
    """Estimation of two-level nested logit using the BFGS procedure."""
    
    range_mu = (0.1, 6.0)
    _epsilon = 0.001 # Step size for approximation of the first derivative
    _approximate_second_derivative = False # If True, the inverse Hessian is computed by a numerical approximation
                                           # of the second derivative (using finite difference method), 
                                           # instead of taking it out of the scipy BFGS function, which seems to be 
                                           # quite sensitive to the _epsilon value.
    
    def run(self, data, upc_sequence, resources):
        """
        'data' is a 4D array (nobservations, nchoices, nvariables, number of nests).
 
        'resources' can contain an entry 'starting_values' which is a dictionary where keys are 
        coefficient names and values are either starting values, or tuples with first element being
        the starting value and second element being boolean determining if the coefficient 
        should be estimated (True) or not (False). Scaling parameters in the 'starting_values'
        dictionary should start with '__logsum_' followed by the nest number.
        
        'resources' can contain an entry 'bfgs_approximate_second_derivative' (logical) which determines if
        the inverse Hessian is computed by a numerical approximation of the second derivative 
        (using finite difference method), instead of taking it out of the scipy BFGS function.
        
        'resources' can contain an entry 'bfgs_epsilon' which is the step size for approximation 
        of the first derivative.
        """
        return EstimationProcedure.run_dcm(self, data, upc_sequence, resources)
    
    def estimate_dcm(self, data):
        nobs, alts, nvars, M = data.shape
        self.M = M
        depm = self.resources["chosen_choice"] # matrix (nobs x alts) of 0's and 1's. 1 is on positions of chosen location.
        tags = ["estimate", "result"]
        vl = 2
        coef_names = self.resources.get("coefficient_names", None)
        nest_numbers = self.get_nest_numbers()
        
        index_of_fixed_values = zeros(nvars+M, dtype="bool8")
        fixed_coefs, fixed_values = self.resources.get("fixed_values", (array([]), array([])))
        if (coef_names is not None) and (fixed_coefs.size > 0):
            index_of_fixed_values[get_indices_of_matched_items(coef_names, fixed_coefs)] = True
        index_of_not_fixed_values = logical_not(index_of_fixed_values)
        
        beta=ones(nvars+M).astype(float32)
        beta[-M:] = self.range_mu[1]
        beta[index_of_fixed_values] = fixed_values.astype(beta.dtype)
        l_0beta = zeros(nvars+M).astype(float32)
        l_0beta[-M:] = 1
        l_0 = self.nl_loglikelihood(l_0beta, data, depm)

        ls_idx = arange(nvars, nvars+M)
        for name, sv in self.resources.get("starting_values", {}).items():
            est = True
            if isinstance(sv, tuple) or isinstance(sv, list):
                est = sv[1]
                sv = sv[0]
            if name.startswith('__logsum_'):
                if nest_numbers is not None:
                    idx = ls_idx[where(nest_numbers == int(name[9:]))[0]]
                else:
                    idx = array([ls_idx[int(name[9:])-1]])
            else:
                idx = ematch(coef_names, name)
            beta[idx] = sv
            index_of_fixed_values[idx] = not(est)

        index_of_not_fixed_values = where(logical_not(index_of_fixed_values))[0] 
        index_of_fixed_values = where(index_of_fixed_values)[0]
        
        bounds = index_of_not_fixed_values.size*[(-5.0,5.0)]
        j=0
        for i in range(nvars+M-1, nvars-1, -1):
            if i in index_of_not_fixed_values:
                bounds[index_of_not_fixed_values.size-j-1] = self.range_mu
                j+=1
                
        logger.start_block('BFGS procedure')
        bfgs_result = fmin_l_bfgs_b(self.minus_nl_loglikelihood, beta[index_of_not_fixed_values], pgtol=.01,
                                args=(data, depm, beta[index_of_fixed_values], index_of_not_fixed_values, index_of_fixed_values), 
                                bounds=bounds,approx_grad=True,
                                disp=True, epsilon=self.resources.get('bfgs_epsilon', self._epsilon),
                                )

        logger.end_block()
        beta[index_of_not_fixed_values] = bfgs_result[0].astype(beta.dtype)
        se = zeros(nvars+M)
        tvalues = zeros(nvars+M)
        mingrad = bfgs_result[2]['grad']

        if 0: # hessian is no longer provided by bfgs ## not self.resources.get('bfgs_approximate_second_derivative', self._approximate_second_derivative):
            inv_hessian = bfgs_result[3]
            se[index_of_not_fixed_values] = sqrt(diagonal(inv_hessian))
        else:
            sec_der = approximate_second_derivative(self.minus_nl_loglikelihood, beta[index_of_not_fixed_values],
                                                args=(data, depm, beta[index_of_fixed_values], index_of_not_fixed_values, 
                                                      index_of_fixed_values))
            inv_hessian = 1.0/sec_der
            se[index_of_not_fixed_values] = sqrt(inv_hessian)
        
        tvalues[index_of_not_fixed_values] = beta[index_of_not_fixed_values]/se[index_of_not_fixed_values]
        
        l_1=self.nl_loglikelihood(beta, data, depm)

        ll_ratio = 1-(l_1/l_0)
        adj_ll_ratio = 1-((l_1-nvars-M)/l_0)
        
        # http://en.wikipedia.org/wiki/Akaike_information_criterion 
        aic = 2 * index_of_not_fixed_values.size - 2 * l_1
        logger.log_status("Akaike's Information Criterion (AIC): ", str(aic), tags=tags, verbosity=vl)
        bic = -2 * l_1 + index_of_not_fixed_values.size * log(nobs)
        logger.log_status("Bayesian Information Criterion (BIC): ", str(bic), tags=tags, verbosity=vl)
        logger.log_status("***********************************************", tags=tags, verbosity_level=vl)
        logger.log_status('Log-likelihood is:           ', l_1, tags=tags, verbosity_level=vl)
        logger.log_status('Null Log-likelihood is:      ', l_0, tags=tags, verbosity_level=vl)
        logger.log_status('Likelihood ratio index:      ', ll_ratio, tags=tags, verbosity_level=vl)
        logger.log_status('Adj. likelihood ratio index: ', adj_ll_ratio, tags=tags, verbosity_level=vl)
        logger.log_status('Number of observations:      ', nobs, tags=tags, verbosity_level=vl)
        logger.log_status('Suggested |t-value| >        ', sqrt(log(nobs)))
        logger.log_status('WARNING: Standard errors printed below are approximated')
        logger.log_status("-----------------------------------------------", tags=tags, verbosity_level=vl)
        if coef_names is not None:
            nestn = nest_numbers
            if nestn is None:
                nestn = list(range(1,M+1))
            names = concatenate((coef_names, array(['__logsum_%s' % x for x in nestn])))
        else:
            names = ['']*(nvars+M)
        logger.log_status("Coeff_names\testimate\tstd err\t\tt-values\tgradient", tags=tags, verbosity_level=vl)
        for i in range(index_of_not_fixed_values.size):
            logger.log_status("%10s\t%8g\t%8g\t%8g\t%8g" % (names[index_of_not_fixed_values[i]],
                                                            beta[index_of_not_fixed_values[i]],
                                                            se[index_of_not_fixed_values[i]],
                                                            tvalues[index_of_not_fixed_values[i]], mingrad[i]), 
                              tags=tags, verbosity_level=vl)
        logger.log_status('***********************************************', tags=tags, verbosity_level=vl)
        logger.log_status('Elapsed time: ',time.perf_counter()-self.start_time, 'seconds', tags=tags, verbosity_level=vl)
        df=nvars+M-index_of_fixed_values.size
        lrts = -2*(l_0-l_1)
        return {"estimators":beta, "coefficient_names": names, "standard_errors":se, "other_measures":{"t_statistic": tvalues},
                 "other_info":{"p-value":chisqprob(lrts, df),
                    "ll_ratio_index":ll_ratio,
                    "ll_ratio_test_statistics":lrts, "df": df,  "nobs":nobs}}

    def nl_loglikelihood(self, b, data, depm):
        return EstimationProcedure.dcm_loglikelihood(self, data, b, depm)

    def minus_nl_loglikelihood(self, b, data, depm, b_fixed, index_of_not_fixed_values, index_of_fixed_values):
        # used in a minimizing routine
        coef = zeros(b.size + b_fixed.size)
        coef[index_of_not_fixed_values] = b.astype(coef.dtype)
        coef[index_of_fixed_values] = b_fixed
        a = -1*self.nl_loglikelihood(coef, data, depm)
        #print "coefficients = ", coef
        #print a
        return a
        
    def get_nest_numbers(self):
        model = self.resources.get('_model_')
        if model is None:
            return None
        if not 'get_nested_structure' in dir(model):
            return None
        return sort(list(model.get_nested_structure().keys()))

def approximate_second_derivative(f, x, args):
    delta = 0.001*x
    mu = identity(delta.size, dtype='bool8')
    result = zeros(delta.size)
    delta_square = delta*delta
    for i in range(result.size):
        result[i] = (f(x+2*delta[i]*mu[:,i], *args)-2*f(x+delta[i]*mu[:,i], *args) + f(x, *args))/delta_square[i]
    return result

