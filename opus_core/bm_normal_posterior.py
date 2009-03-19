# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from numpy import reshape, sum, where, sqrt
from numpy.random import normal

class bm_normal_posterior:
    """ Class for computing posterior distribution for Bayesian melding as a mixture of normal components."""
    def run(self, bm_object, replicates=100, truncate_at_zero=True, **kwargs):
        pmean = bm_object.get_posterior_component_mean()
        K, I = pmean.shape
        variance = bm_object.get_posterior_component_variance()
        weights = bm_object.get_weights()
        rns = normal(reshape(pmean, (K, I, 1)), reshape(sqrt(variance), (1, I, 1)),
                     (K, I, replicates))
        result = sum(reshape(weights, (1,I,1)) * rns, axis=1)
        if truncate_at_zero:
            result[where(result < 0)] = 0
        return result


