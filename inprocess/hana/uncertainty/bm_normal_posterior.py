#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

from numpy import reshape, sum, where, sqrt
from numpy.random import normal
from opus_core.logger import logger

class bm_normal_posterior:
    """ Class for computing posterior distribution for Bayesian melding as a mixture of normal components."""
    def run(self, bm_object, replicates=100, truncate_at_zero=True, **kwargs):
        pmean = bm_object.get_posterior_component_mean()
        K, I = pmean.shape
        variance = bm_object.get_posterior_component_variance()
        weights = bm_object.get_weights()
        rnN01 = normal(0,1, (K, I, replicates))
        #logger.log_status("RNs:") 
        #logger.log_status("**********")
        #logger.log_status(rnN01[0:50,0,0])
        rns = reshape(pmean, (K, I, 1)) + reshape(sqrt(variance), (1, I, 1)) * rnN01
        result = sum(reshape(weights, (1,I,1)) * rns, axis=1)
        if truncate_at_zero:
            result[where(result < 0)] = 0
        return result


