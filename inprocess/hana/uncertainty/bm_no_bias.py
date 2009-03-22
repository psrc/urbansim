# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.bayesian_melding import BayesianMeldingFromFile

class BmNoBias(BayesianMeldingFromFile):
    """ Like BayesianMeldingFromFile, but does not include bias.
    """
        
    def get_bias_for_quantity(self):
        return 0
