# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.bayesian_melding import BayesianMeldingFromFile

class BmNoVarpf(BayesianMeldingFromFile):
    """ Like BayesianMeldingFromFile, but does not include propagation factor of the variance.
    """
    
    def get_posterior_component_variance(self):
        return self.get_variance_for_quantity()

