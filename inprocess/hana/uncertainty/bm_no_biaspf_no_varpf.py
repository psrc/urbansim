# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.bayesian_melding import BayesianMeldingFromFile

class BmNoBiaspfNoVarpf(BayesianMeldingFromFile):
    """ Like BayesianMeldingFromFile, but does not include any propagation factor.
    """
    
    def set_propagation_factor(self, year):
        self.propagation_factor = 1

