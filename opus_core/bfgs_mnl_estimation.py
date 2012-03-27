# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.estimation_procedure import EstimationProcedure
from opus_core.logger import logger
from numpy import zeros,log,transpose,float32,dot,reshape,diagonal,sqrt, repeat, squeeze
from numpy import array, ones, where, arange, exp, in1d, newaxis, logical_not, newaxis
from numpy.linalg import inv
from opus_core.third_party.pstat import chisqprob
from opus_core.misc import get_indices_of_matched_items
from opus_core.bhhh_mnl_estimation import bhhh_mnl_estimation
from scipy.optimize import fmin_l_bfgs_b
from numpy.core.umath_tests import inner1d
from numpy.core.umath_tests import matrix_multiply

import time
#import pdb

class bfgs_mnl_estimation(bhhh_mnl_estimation):
    dtype = float32
    maxiter = 20000
    epsilon = 1e-8 ##step size used when approx_grad is true, 
                   ##for numerically calculating the gradient
    approx_grad=0 
    iprint = -1

    def estimate_dcm(self, data):
        nobs, alts, nvars = data.shape
        # matrix (nobs x alts) of 0's and 1's. 1 is on positions of chosen location.
        depm = self.resources["chosen_choice"] 
        coef_names = self.resources.get("coefficient_names", None)
        tags = ["estimate", "result"]
        vl = 2
        
        is_fixed_values = zeros(nvars, dtype="bool")
        fixed_coefs, fixed_values = self.resources.get("fixed_values", 
                                                      (array([]), array([])))
        if (coef_names is not None) and (fixed_coefs.size > 0):
            is_fixed_values[in1d(coef_names, fixed_coefs)] = True
        is_unfixed_values = logical_not(is_fixed_values)

        if is_fixed_values.sum() > 0:
            logger.log_warning("fixed coefficients have not been tested with BFGS estimation procedure; ")
            logger.log_warning("use with caution!")

        beta=zeros(nvars, dtype=self.dtype)
        beta[is_fixed_values] = fixed_values.astype(beta.dtype)
        ll_0=self.loglikelihood(beta, data, depm)

        bounds_lower = bounds_upper = repeat([None], beta.size)
        bounds_lower[is_fixed_values] = bounds_upper[is_fixed_values] = fixed_values
        bounds = zip(bounds_lower, bounds_upper)
                
        logger.start_block('Starting L_BFGS_B procedure...')
        epsilon = self.resources.get('bfgs_epsilon', self.epsilon)
        fprime = self.get_gradient if not self.approx_grad else None
        bfgs_result = fmin_l_bfgs_b(self.minus_loglikelihood, beta, 
                                    args=(data, depm), 
                                    fprime=self.get_gradient,
                                    approx_grad=self.approx_grad, 
                                    bounds=bounds, 
                                    iprint=self.iprint, 
                                    epsilon=epsilon,
                                    maxfun=self.maxiter
                                    )

        beta = bfgs_result[0].astype(beta.dtype)
        func_at_min = bfgs_result[1]
        info = bfgs_result[2]
        status = {0:'Convergence achieved.', 
                  1:'Maximum iterations reached without convergence.',
                  2:'Stop for another reason: %s.' % info['task'] if info.has_key('task') \
                                                                  else 'unknown'
                 }
        warnflag = ''
        if info['warnflag'] != 0:
            warnflag = status[info['warnflag']]

        grad_at_min = info['grad']
        g = self.get_gradient_by_agent(beta, data, depm)
        try:
            h=self.get_hessian(g)
        except:
            msg = "Estimation led to singular matrix. No results."
            warnflag += msg + "\n"
            logger.log_warning(msg, tags=tags, verbosity_level=vl)
            return {}

        g=g.sum(axis=0)
        c=dot(dot(transpose(g),h),g)

        se=(self.get_standard_error(h)).astype(self.dtype)
        se[is_fixed_values] = 0.0
        tvalues=zeros(nvars, dtype=self.dtype)

 
        tvalues[is_unfixed_values] = beta[is_unfixed_values]/se[is_unfixed_values]
        
        ll_1=self.loglikelihood(beta, data, depm)
        ll_ratio = 1-(ll_1/ll_0)
        adj_ll_ratio = 1-((ll_1-nvars)/ll_0)
        
        # http://en.wikipedia.org/wiki/Akaike_information_criterion 
        aic = 2 * is_unfixed_values.size - 2 * ll_1
        bic = -2 * ll_1 + is_unfixed_values.size * log(nobs)
        df=nvars-is_fixed_values.sum()
        lrts = -2*(ll_0-ll_1)
        iters = info['funcalls']

        results = {"coefficient_names":coef_names,
                  "estimators":beta, 
                  "standard_errors":se, 
                  "other_measures":{"t_statistic": tvalues},
                  "other_info":{"aic": aic,
                                "bic": bic,
                                "p-value":chisqprob(lrts, df),
                                "l_0": ll_0,
                                "l_1": ll_1,
                                "ll_ratio_index":ll_ratio,
                                "ll_ratio_test_statistics":lrts,
                                "convergence": c,
                                "df": df,  
                                "nobs":nobs,
                                "nvars": nvars,
                                "nalts": alts,
                                "iterations": iters
                                },
                   "warnflag": warnflag
                  }
        self.print_results(results)
        logger.end_block()
        #logger.log_status('Elapsed time: ', time.clock()-self.start_time, 'seconds',
        #                  tags=tags, verbosity_level=vl)
        return results

    def loglikelihood(self, beta, data, depm):
        return EstimationProcedure.dcm_loglikelihood(self, data, beta, depm)
        #return EstimationProcedure.dcm_loglikelihood(self, data=data, beta=beta, depm=depm)

    def minus_loglikelihood(self, *arg, **kwargs):
        return -self.loglikelihood(*arg, **kwargs)

    def get_gradient_by_agent(self, beta, data, depm):
        nobs, alts, nvars = data.shape
        self.upc_sequence.compute_utilities(data, beta, self.resources)
        p = self.upc_sequence.compute_probabilities(self.resources)
        d = (depm - p)
        ## WAS: g0 = (d[..., newaxis] * data).sum(axis=1)
        g = matrix_multiply(d[:,newaxis,:], data)
        g = squeeze(g)
        return g

    def get_gradient(self, beta, data, depm):
        #import ipdb; ipdb.set_trace()
        grad = self.get_gradient_by_agent(beta, data, depm)
        grad = grad.sum(axis=0)
        return -grad

    def get_hessian(self, derivative):
        return inv(dot(transpose(derivative),derivative))

    def get_standard_error(self, hessian):
        return sqrt(diagonal(self.get_covariance(hessian)))
        
    def get_covariance(self, hessian):
        return hessian

