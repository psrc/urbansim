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
        for l in y_all.keys():
            y = y_all[l]
            mu = mu_all[l]
            K = y.size
            variance = variance_all[l]
            bias = bias_all[l]
            tmp1 = -K/2.0 * log(2.0*pi*variance)
            tmp2 = sum((reshape(y, (y.size,1)) - bias - mu)**2.0, axis=0)/(2.0*variance)
            logwi = tmp1 - tmp2
            logwi = logwi - logwi.max()
            wi = wi * exp(logwi)
        return wi/wi.sum()