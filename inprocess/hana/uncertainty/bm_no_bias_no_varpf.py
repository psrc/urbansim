# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.bayesian_melding import BayesianMelding
from opus_core.bayesian_melding import BayesianMeldingFromFile


class BayesianMeldingNoBiasNoVarpf(BayesianMelding):
    """ Like BayesianMelding, but does not include bias and propagation factor of the variance.
    """
    
    def set_propagation_factor(self, year):
        self.propagation_factor = 1
        
    def get_bias_for_quantity(self):
        return 0
    
    
class BmNoBiasNoVarpf(BayesianMeldingFromFile):
    """ Like BayesianMeldingFromFile, but does not include bias and propagation factor of the variance.
    """
    
    def set_propagation_factor(self, year):
        self.propagation_factor = 1
        
    def get_bias_for_quantity(self):
        return 0

