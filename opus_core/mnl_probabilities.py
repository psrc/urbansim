# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

#
from numpy import exp, reshape, where, arange, array, newaxis, sum
from numpy import ma
from scipy.ndimage import sum as ndimage_sum
from opus_core.probabilities import Probabilities
from opus_core.misc import unique_values
from opus_core.logger import logger

class mnl_probabilities(Probabilities):

    computable_range = (-87.0, 87.0)   # float32
#    computable_range = (-703.0, 703.0) # float64

    def run(self, utilities, resources=None):
        """ Compute probabilities of a discrete choice model from the given utitlities.
        'utilities' is a 2D array (nobservations x nequations).
        The return value is a 2D array (same shape as utilities).
        """
        if utilities.ndim < 2:
            raise StandardError, "Argument 'utilities' must be a 2D numpy array."

        util_min = utilities.min()
        util_max = utilities.max()
        if (util_min < self.computable_range[0]) or (util_max > self.computable_range[1]):
            # shift utilities to zero (maximum is at zero)
            to_be_transformed=where((utilities < self.computable_range[0]) + (utilities > self.computable_range[1]))
            to_be_transformed=unique_values(to_be_transformed[0])
            for idx in arange(to_be_transformed.size):
                i = to_be_transformed[idx]
                this_max = utilities[i,:].max()
                utilities[i,:]=utilities[i,:]-this_max

        exponentiated_utility = exp(utilities)
        sum_exponentiated_utility = sum(exponentiated_utility, axis=1, dtype="float64")
        return exponentiated_utility/reshape(sum_exponentiated_utility,(utilities.shape[0], 1))

    def get_demand(self, index, probability, nsupply):
        flat_index = index.ravel()
        l = flat_index + 1
        demand = array(ndimage_sum(probability.ravel(), labels=l, index=arange(nsupply)+1))
        return demand

    def get_omega(self, probability, constrained_locations_matrix, sdratio_matrix):

        prob_sum = 1-sum(probability*constrained_locations_matrix,1)
        #prob_sum = sum(probability*unconstrained_locations_matrix, axis=1)
        # The recoding of prob_sum and omega are to handle extreme values of omega and zero divide problems
        # A complete solution involves stratifying the choice set in the initialization to ensure that
        # there are always a mixture of constrained and unconstrained alternatives in each choice set.
        if where(prob_sum==0)[0].size > 0:
            logger.log_warning("There are zeros in sum of unconstrained locations",
                                tags=["probabilities", "logit"])
        #prob_sum = where(prob_sum==0,-1,prob_sum)

        omega = (1-sum(probability*constrained_locations_matrix*sdratio_matrix,1))/prob_sum
        ##should we use sdratio_matrix or sdratio?
        #omega = (1-sum(probability*constrained_locations_matrix*sdratio,1))/prob_sum

        #omega = where(omega>5,5,omega)
        #omega = where(omega<.5,5,omega)
        #omega = where(prob_sum<0,5,omega)
        return omega

    def get_pi(self, sdratio_matrix, omega, constrained_locations_matrix):
        #pi = sdratio_matrix / omega[:,newaxis] * constrained_locations_matrix + unconstrained_locations_matrix
        pi = sdratio_matrix * constrained_locations_matrix + omega[:, newaxis] * (1 - constrained_locations_matrix)
        return pi

    def get_average_omega(self, omega, probability, index, nsupply, demand):
        omega_prob = omega[:, newaxis]*probability
        omega_prob_sum_over_i = array(ndimage_sum(omega_prob, labels=index+1, index=arange(nsupply)+1))
        prob_sum_over_i = array(ndimage_sum(probability, labels=index+1, index=arange(nsupply)+1))
        average_omega = ma.filled(omega_prob_sum_over_i/
                      ma.masked_where(prob_sum_over_i==0, prob_sum_over_i), 0.0)
        return average_omega
