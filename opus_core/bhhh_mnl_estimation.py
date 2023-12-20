# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.estimation_procedure import EstimationProcedure
from opus_core.logger import logger
from numpy import zeros,log,transpose,float32,dot,reshape,diagonal,sqrt
from numpy import array, ones, where, arange, exp, newaxis
from numpy.linalg import inv
from opus_core.third_party.pstat import chisqprob
from opus_core.misc import get_indices_of_matched_items
import time
#import pdb

class bhhh_mnl_estimation(EstimationProcedure):
    maximum_iterations = 200
    
    def print_results(self, result, tags=["estimate", "result"], verbosity_level=2):
        model_info = result['other_info']
        aic = model_info['aic']
        bic = model_info['bic']
        iterations = model_info['iterations']
        l_1 = model_info['l_1']
        l_0 = model_info['l_0']
        ll_ratio = model_info['ll_ratio_index']
        nobs = model_info['nobs']
        nvars = model_info['nvars']
        nalts = model_info['nalts']
        c = model_info['convergence']
        adj_ll_ratio = 1-((l_1-nvars)/l_0)
        
        names = result['coefficient_names']
        b1 = result['estimators']
        se = result['standard_errors']
        tvalues = result["other_measures"]["t_statistic"]
        warnflag = result["warnflag"]
        
        logger.log_status("Akaike's Information Criterion (AIC): ", str(aic), tags=tags, verbosity=verbosity_level)
        logger.log_status("Bayesian Information Criterion (BIC): ", str(bic), tags=tags, verbosity=verbosity_level)
        
        logger.log_status("Number of Iterations: ", iterations, tags=tags, verbosity_level=verbosity_level)
        logger.log_status("***********************************************", tags=tags, verbosity_level=verbosity_level)
        logger.log_status('Log-likelihood is:           ', l_1, tags=tags, verbosity_level=verbosity_level)
        logger.log_status('Null Log-likelihood is:      ', l_0, tags=tags, verbosity_level=verbosity_level)
        logger.log_status('Likelihood ratio index:      ', ll_ratio, tags=tags, verbosity_level=verbosity_level)
        logger.log_status('Adj. likelihood ratio index: ', adj_ll_ratio, tags=tags, verbosity_level=verbosity_level)
        logger.log_status('Number of observations:      ', nobs, tags=tags, verbosity_level=verbosity_level)
        logger.log_status('Number of alternatives:      ', nalts, tags=tags, verbosity_level=verbosity_level)        
        logger.log_status('Suggested |t-value| >        ', sqrt(log(nobs)))
        logger.log_status('Convergence statistic is:    ', c, tags=tags, verbosity_level=verbosity_level)
        logger.log_status("-----------------------------------------------", tags=tags, verbosity_level=verbosity_level)

        logger.log_status("Coeff_names\testimate\tstd err\t\tt-values", tags=tags, verbosity_level=verbosity_level)
        for i in arange(nvars):
            logger.log_status("%10s\t%8g\t%8g\t%8g" % (names[i],b1[i],se[i],tvalues[i]), tags=tags, verbosity_level=verbosity_level)
        logger.log_status('***********************************************', tags=tags, verbosity_level=verbosity_level)
        if warnflag:
            logger.log_warning(warnflag, tags=tags, verbosity_level=verbosity_level)
        #logger.log_status('Elapsed time: ',time.perf_counter()-self.start_time, 'seconds', tags=tags, verbosity_level=verbosity_level)

        
    def run(self, data, upc_sequence, resources):
        """
        'data' is of shape (nobservations, nchoices, nvariables).
        """
        return EstimationProcedure.run_dcm(self, data, upc_sequence, resources)
        
    def estimate_dcm(self, data):
        maxiter=self.maximum_iterations #Maximum iterations allowed
        eps=0.001 #Convergence criterion for gradient*hessian-inv*gradient
        tags = ["estimate", "result"]
        vl = 2
        nobs, alts, nvars = data.shape
        depm = self.resources["chosen_choice"] # matrix (nobs x alts) of 0's and 1's. 1 is on positions of chosen location.
        coef_names = self.resources.get("coefficient_names", None)
        fixed_coefs, fixed_values = self.resources.get("fixed_values", (array([]), array([])))
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
        se = zeros(nvars).astype(float32)
        tvalues = zeros(nvars).astype(float32)
        l_2=self.mnl_loglikelihood(data, b2, depm)
        l_0 = l_2
        s=1
        warnflag = ''

        for it in range(maxiter):
            b1=b2
            l_1=l_2
            g=(self.mnl_gradient(data, b1, depm, index_of_not_fixed_values))
            try:
                h=self.get_hessian(g)
            except:
                msg = "Estimation led to singular matrix. No results."
                warnflag += msg + "\n"
                logger.log_warning(msg, tags=tags, verbosity_level=vl)
                return {}
            g=g.sum(axis=0)
            c=dot(dot(transpose(g),h),g)
            if c <= eps:
                msg = "Convergence achieved."
                logger.log_status(msg, tags=tags, verbosity_level=vl)
                break
            d=dot(h,g)
            b2[index_of_not_fixed_values]=(b1[index_of_not_fixed_values]+s*d).astype(b2.dtype)
            l_2=self.mnl_loglikelihood(data,b2, depm)
            if l_2 <= l_1:
                s=s/2.0
            if s <= .001:
                msg = "Cannot find increase."
                warnflag += msg + "\n"
                #logger.log_warning(msg, tags=tags, verbosity_level=vl)
                break
        # end of the iteration loop
        
        if it>=(maxiter-1):
            msg = "Maximum iterations reached without convergence."
            warnflag += msg + "\n"
            #logger.log_warning(msg, tags=tags, verbosity_level=vl)
 
        se[index_of_not_fixed_values]=self.get_standard_error(h).astype(se.dtype)
        tvalues[index_of_not_fixed_values] = (b1[index_of_not_fixed_values]/se[index_of_not_fixed_values]).astype(tvalues.dtype)
        ll_ratio = 1-(l_1/l_0)
        adj_ll_ratio = 1-((l_1-nvars)/l_0)
        
        # http://en.wikipedia.org/wiki/Akaike_information_criterion 
        aic = 2 * index_of_not_fixed_values.size - 2 * l_1
        bic = -2 * l_1 + index_of_not_fixed_values.size * log(nobs)

        if coef_names is not None:
            names = coef_names
        else:
            names = ['']*index_of_not_fixed_values.size

        est = b1
        df=nvars-index_of_fixed_values.size
        lrts = -2*(l_0-l_1)

        result = {"coefficient_names":names,
                  "estimators":est, 
                  "standard_errors":se, 
                  "other_measures":{"t_statistic": tvalues},
                  "other_info":{"aic": aic,
                                "bic": bic,
                                "p-value":chisqprob(lrts, df),
                                "l_0": l_0,
                                "l_1": l_1,
                                "ll_ratio_index":ll_ratio,
                                "ll_ratio_test_statistics":lrts,
                                "convergence": c,
                                "df": df,  
                                "nobs":nobs,
                                "nvars": nvars,
                                "nalts": alts,
                                "iterations": it+1
                                },
                  "warnflag": warnflag}
        self.print_results(result)
        
        return result

    def mnl_loglikelihood(self, data, b, depm):
        return EstimationProcedure.dcm_loglikelihood(self, data, b, depm)

    def mnl_gradient(self, data, b, depm, index_of_not_fixed_values):
        nobs, alts, nvars = data.shape
        self.upc_sequence.compute_utilities(data, b, self.resources)
        p = self.upc_sequence.compute_probabilities(self.resources)
        d = (depm - p)

        #g = (reshape((reshape(d,(nobs*alts,1))*reshape(data[:,:,index_of_not_fixed_values], 
        #                                   (nobs*alts,index_of_not_fixed_values.size))),
        #                                 (nobs,alts,index_of_not_fixed_values.size))).sum(axis=1)

        g = (d[..., newaxis] * data[..., index_of_not_fixed_values]).sum(axis=1)
        return g

    def get_hessian(self, derivative):
        return inv(dot(transpose(derivative),derivative))
        
    def get_standard_error(self, hessian):
        return sqrt(diagonal(self.get_covariance(hessian)))
        
    def get_covariance(self, hessian):
        return hessian
