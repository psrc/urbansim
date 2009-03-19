# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.bayesian_melding import BayesianMeldingFromFile

class BmNoBias(BayesianMeldingFromFile):
    """ Like BayesianMeldingFromFile, but does not include bias.
    """
        
    def get_bias_for_quantity(self):
        return 0
