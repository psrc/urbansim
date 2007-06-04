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
from opus_core.logger import logger
from numpy import zeros,log,transpose,float32,dot,reshape,diagonal,sqrt, array, ones, where, arange
from numpy.linalg import inv
from opus_core.pstat import chisqprob
from opus_core.misc import get_indices_of_matched_items
import time
#import pdb

class bhhh_mnl_estimation(EstimationProcedure):
    def run(self, data, upc_sequence, resources):
        """
        'data' is of shape (nobservations, nchoices, nvariables).
        """
        start= time.clock()
        maxiter=200 #Maximum iterations allowed
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
                h=inv(dot(transpose(g),g))
            except:
                logger.log_warning("Estimation led to singular matrix. No results.", tags=tags, verbosity_level=vl)
                return {}
            g=g.sum(axis=0)
            c=dot(dot(transpose(g),h),g)
            dhinv=diagonal(h)
            se[index_of_not_fixed_values]=(sqrt(diagonal(h))).astype(se.dtype)
            ll_ratio = 1-(l_1/l_0)
            adj_ll_ratio = 1-((l_1-nvars)/l_0)
            tvalues[index_of_not_fixed_values] = (b1[index_of_not_fixed_values]/se[index_of_not_fixed_values]).astype(tvalues.dtype)
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
        if it>=(maxiter-1):
            logger.log_warning('Maximum iterations reached without convergence', tags=tags, verbosity_level=vl)
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
