# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
#

import numpy as np
from opus_core.upc.mnl_probabilities import mnl_probabilities

class annualized_disappearance_probabilities(mnl_probabilities):
    years = 4

    def run(self, *args, **kwargs):
        """
        """
	prob = mnl_probabilities.run(self, *args, **kwargs)
	annualized_prob = 1 - np.power(1-prob, 1.0/self.years)

        return annualized_prob

