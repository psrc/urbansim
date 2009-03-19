# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.bayesian_melding import BayesianMeldingFromFile

class BmNoBiaspf(BayesianMeldingFromFile):
    """ Like BayesianMeldingFromFile, but does not include propagation factor of the bias.
    """
    
    def get_posterior_component_mean(self):
        return self.get_bias_for_quantity() + self.get_predicted_values()