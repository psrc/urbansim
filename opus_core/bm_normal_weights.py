# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import log, sum, exp, reshape, float32, ones
from math import pi

class bm_normal_weights:
    """ Class for computing normally distributed weights for Bayesian melding."""
    def run(self, bm_object, **kwargs):
        y_all = bm_object.get_data()
        mu_all = bm_object.get_expected_values()
        variance_all = bm_object.get_variance()
        bias_all = bm_object.get_bias()
        wi = ones(bm_object.number_of_runs, dtype=float32)
        weight_components = {}
        for l in y_all.keys():
            y = y_all[l]
            mu = mu_all[l]
            K = y.size
            variance = variance_all[l]
            bias = bias_all[l]
            tmp1 = -K/2.0 * log(2.0*pi*variance)
            #tmp2 = sum((reshape(y, (y.size,1)) - bias - mu)**2.0, axis=0)/(2.0*variance)
            tmp2 = sum((reshape(y, (y.size,1)) - reshape(bias, (bias.size,1)) - mu)**2.0, axis=0)/(2.0*variance)
            logwi = tmp1 - tmp2
            logwi = logwi - logwi.max()
            this_wi = exp(logwi)
            weight_components[l] = this_wi/this_wi.sum()
            wi = wi * weight_components[l]
        return (wi/wi.sum(), weight_components)