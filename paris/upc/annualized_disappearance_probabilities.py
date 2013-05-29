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
        estimate = False
        if 'resources' in kwargs:
            resources = kwargs['resources']
            estimate = resources.get('estimate', False)

        if not estimate:
            ## annualized prob for simulation
            #original implementation: prob = 1 - np.power(1-prob, 1.0/self.years)
            annual_dis_prob = 1 - np.power(1 - prob[:,1], 1.0/self.years)
            prob[:,1] = annual_dis_prob
            prob[:,0] = 1 - annual_dis_prob
        
        #adjusted_prob = prob[:,1]/4
        #prob[:,1] = adjusted_prob
        #prob[:,0] = 1 - adjusted_prob
        
        return prob

