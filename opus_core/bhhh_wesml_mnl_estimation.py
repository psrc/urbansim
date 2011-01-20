# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.bhhh_mnl_estimation import bhhh_mnl_estimation
from opus_core.logger import logger
from numpy import zeros,log,transpose,float32,dot,reshape,diagonal,sqrt, array, ones, where, arange
from numpy.linalg import inv
from opus_core.third_party.pstat import chisqprob
from opus_core.misc import get_indices_of_matched_items
import time
#import pdb

class bhhh_wesml_mnl_estimation(bhhh_mnl_estimation):
    maximum_iterations = 1000 # converges slower than ordinary MLE
    
    def run(self, data, upc_sequence, resources):
        """
        'data' is of shape (nobservations, nchoices, nvariables).
        WESML procedure (Weighted endogenous sampling maximum likelihood), Manski, Lerman 1977
        data are weighted by correction weights (observation_share/sampled_share) in order to take into account 
        undersampled or oversampled observations.
        Set the variable name for the correction weights into estimate_config (in choice_model) as 
        "wesml_sampling_correction_variable" entry.
        """
        model = resources.get("_model_")
        self.wesml_weights = model.choice_set.compute_variables([resources.get("wesml_sampling_correction_variable")], 
                                           dataset_pool=model.dataset_pool)
        self.wesml_weights = self.wesml_weights[resources.get("index")]
        weighted_data = data*reshape(self.wesml_weights, (data.shape[0], data.shape[1], 1))
        return bhhh_mnl_estimation.run(self, weighted_data, upc_sequence, resources)

    def mnl_gradient(self, data, b, depm, index_of_not_fixed_values):
        """Like mnl_gradient in bhhh, but it keeps the value of the derivative before summing, in order to 
        reuse it in the computation of the covariance.
        """
        nobs, alts, nvars = data.shape
        self.upc_sequence.compute_utilities(data, b, self.resources)
        p = self.upc_sequence.compute_probabilities(self.resources)
        d = depm - p
        self.non_weighted_derivative = reshape((reshape(d,(nobs*alts,1))*reshape(data[:,:,index_of_not_fixed_values], 
                                           (nobs*alts,index_of_not_fixed_values.size))),
                                         (nobs,alts,index_of_not_fixed_values.size))
        return self.non_weighted_derivative.sum(axis=1)
            
    def get_covariance(self, hessian):
        """Covariance adjusted as suggested by Ben-Akiva, Lerman, 1985 (pp 239)."""
        weighted_derivative = (reshape(self.wesml_weights, (self.wesml_weights.shape[0], self.wesml_weights.shape[1], 1)) * \
                            self.non_weighted_derivative).sum(axis=1)
        weighted_hessian = dot(transpose(weighted_derivative), self.non_weighted_derivative.sum(axis=1))
        return dot(dot(hessian,weighted_hessian),hessian)
        