# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.estimation_procedure import EstimationProcedure
from opus_core.logger import logger
from numpy import zeros,log,transpose,float32,dot,reshape,diagonal,sqrt, array, ones, where, arange, exp
from numpy.linalg import inv
from opus_core.pstat import chisqprob
from opus_core.misc import get_indices_of_matched_items
import time
#import pdb

class bhhh_mnl_estimation(EstimationProcedure):
    maximum_iterations = 200
    minimum_probability = exp(-745.)
    
    def run(self, data, upc_sequence, resources):
        """
        'data' is of shape (nobservations, nchoices, nvariables).
        """
        start= time.clock()
        maxiter=self.maximum_iterations #Maximum iterations allowed
        eps=0.001 #Convergence criterion for gradient*hessian-inv*gradient
        tags = ["estimate", "result"]
        vl = 2
        nobs, alts, nvars = data.shape
        depm = resources["selected_choice"] # matrix (nobs x alts) of 0's and 1's. 1 is on positions of chosen location.
        coef_names = resources.get("coefficient_names", None)
        fixed_coefs, fixed_values = resources.get("fixed_values", (array([]), array([])))
        if (coef_names is not None) and (fixed_coefs.size > 0):
            index_of_fixed_values = get_indices_of_matched_items(coef_names, fixed_coefs)
            index_of_not_fixed_values = ones(nvars, dtype="bool8")
            index_of_not_fixed_values[index_of_fixed_values] = False
            index_of_not_fixed_values = where(index_of_not_fixed_values)[0]
        else:
            index_of_fixed_values = array([], dtype="int32")
            index_of_not_fixed_values = arange(nvars)
#        pdb.set_trace()
        b2=zeros(nvars).astype(float32)
        b2[index_of_fixed_values] = fixed_values.astype(b2.dtype)
        self.upc_sequence=upc_sequence
        
        se = zeros(nvars).astype(float32)
        tvalues = zeros(nvars).astype(float32)
        self.resources = resources
        l_2=self.mnl_loglikelihood(data, b2, depm).sum()
        l_0 = l_2
        s=1

        for it in range(maxiter):
            b1=b2
            l_1=l_2
            g=(self.mnl_gradient(data, b1, depm, index_of_not_fixed_values))
            try:
                h=self.get_hessian(g)
            except:
                logger.log_warning("Estimation led to singular matrix. No results.", tags=tags, verbosity_level=vl)
                return {}
            g=g.sum(axis=0)
            c=dot(dot(transpose(g),h),g)
            if c <= eps:
                logger.log_status('Convergence achieved.', tags=tags, verbosity_level=vl)
                break
            d=dot(h,g)
            b2[index_of_not_fixed_values]=(b1[index_of_not_fixed_values]+s*d).astype(b2.dtype)
            l_2=self.mnl_loglikelihood(data,b2, depm).sum()
            if l_2 <= l_1:
                s=s/2.0
            if s <= .001:
                logger.log_warning('Cannot find increase', tags=tags, verbosity_level=vl)
                break
        # end of the iteration loop
        
        if it>=(maxiter-1):
            logger.log_warning('Maximum iterations reached without convergence', tags=tags, verbosity_level=vl)
 
        se[index_of_not_fixed_values]=self.get_standard_error(h).astype(se.dtype)
        tvalues[index_of_not_fixed_values] = (b1[index_of_not_fixed_values]/se[index_of_not_fixed_values]).astype(tvalues.dtype)
        ll_ratio = 1-(l_1/l_0)
        adj_ll_ratio = 1-((l_1-nvars)/l_0)
        
        # http://en.wikipedia.org/wiki/Akaike_information_criterion 
        aic = 2 * nvars - 2 * l_1
        logger.log_status("Akaike's Information Criterion (AIC): ", str(aic), tags=tags, verbosity=vl)
        
        logger.log_status("Number of Iterations: ", it+1, tags=tags, verbosity_level=vl)
        logger.log_status("***********************************************", tags=tags, verbosity_level=vl)
        logger.log_status('Log-likelihood is:           ', l_1, tags=tags, verbosity_level=vl)
        logger.log_status('Null Log-likelihood is:      ', l_0, tags=tags, verbosity_level=vl)
        logger.log_status('Likelihood ratio index:      ', ll_ratio, tags=tags, verbosity_level=vl)
        logger.log_status('Adj. likelihood ratio index: ', adj_ll_ratio, tags=tags, verbosity_level=vl)
        logger.log_status('Number of observations:      ', nobs, tags=tags, verbosity_level=vl)
        logger.log_status('Suggested |t-value| >        ', sqrt(log(nobs)))
        logger.log_status('Convergence statistic is:    ', c, tags=tags, verbosity_level=vl)
        logger.log_status("-----------------------------------------------", tags=tags, verbosity_level=vl)
        if coef_names is not None:
            names = coef_names
        else:
            names = ['']*index_of_not_fixed_values.size
        logger.log_status("Coeff_names\testimate\tstd err\t\tt-values", tags=tags, verbosity_level=vl)
        for i in index_of_not_fixed_values:
            logger.log_status("%10s\t%8g\t%8g\t%8g" % (names[i],b1[i],se[i],tvalues[i]), tags=tags, verbosity_level=vl)
        logger.log_status('***********************************************', tags=tags, verbosity_level=vl)
        logger.log_status('Elapsed time: ',time.clock()-start, 'seconds', tags=tags, verbosity_level=vl)
        est = b1
        df=nvars-index_of_fixed_values.size
        lrts = -2*(l_0-l_1)
        return {"estimators":est, "standard_errors":se, "other_measures":{"t_statistic": tvalues},
                 "other_info":{"p-value":chisqprob(lrts, df),
                    "ll_ratio_index":ll_ratio,
                    "ll_ratio_test_statistics":lrts, "df": df,  "nobs":nobs}}

    def mnl_loglikelihood(self, data, b, depm):
        self.upc_sequence.compute_utilities(data, b, self.resources)
        p = self.upc_sequence.compute_probabilities(self.resources)
        #assure that we can get log from p (replace 0 by minimum  value for 0)
        p[where(p==0)] = self.minimum_probability
        ll = (depm*log(p)).sum(axis=0)
        return ll

    def mnl_gradient(self, data, b, depm, index_of_not_fixed_values):
        nobs, alts, nvars = data.shape
        self.upc_sequence.compute_utilities(data, b, self.resources)
        p = self.upc_sequence.compute_probabilities(self.resources)
        d = (depm - p)
        g = (reshape((reshape(d,(nobs*alts,1))*reshape(data[:,:,index_of_not_fixed_values], 
                                           (nobs*alts,index_of_not_fixed_values.size))),
                                         (nobs,alts,index_of_not_fixed_values.size))).sum(axis=1)
        return g

    def get_hessian(self, derivative):
        return inv(dot(transpose(derivative),derivative))
        
    def get_standard_error(self, hessian):
        return sqrt(diagonal(self.get_covariance(hessian)))
        
    def get_covariance(self, hessian):
        return hessian
