# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import exp, where, log
from opus_core.model_component import ModelComponent
import time

class EstimationProcedure(ModelComponent):
    """ Serves as a parent class for user defined estimation procedures.     
    """
    
    def run_dcm(self, data, upc_sequence=None, resources=None):
        self.start_time = time.clock()
        self.minimum_probability = exp(-745.)
        self.upc_sequence = upc_sequence
        self.resources = resources
        return self.estimate_dcm(data)
        
    def estimate_dcm(self, data):
        assert StandardError, "Method not implemented. It is a responsibility of the child class."
        
    def dcm_loglikelihood(self, data, b, depm):
        self.upc_sequence.compute_utilities(data, b, self.resources)
        p = self.upc_sequence.compute_probabilities(self.resources)
        #assure that we can get log from p (replace 0 by minimum  value for 0)
        p[where(p==0)] = self.minimum_probability
        ll = (depm*log(p)).sum()
        return ll
