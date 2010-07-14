# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.rate_dataset import RateDataset
from opus_core.probabilities import Probabilities
from opus_core.logger import logger
from numpy import array, zeros


class rate_based_probabilities(Probabilities):
    agent_set = ''
    rate_set = ''
    
    def run(self, utilities=None, resources=None):
        """ Return a probability array obtained from a RateDataset. 'resources' must contain
        an entry with name self.rate_set (a RateDataset dataset) and an entry self.agent_set dataset
        that is able to provide attributes defined in rate_set columns. Otherwise the method
        returns equal probability of 0.25.
        """
        if self.agent_set:
            agents = resources.get(self.agent_set, None)
        else:
            agents = resources.get('agent_set', None)
            if agents is not None: self.agent_set = agents.get_dataset_name()
        if agents == None:
            raise RuntimeError("Unable to get agent set " + self.agent_set)

        if self.rate_set:
            rates = resources.get(self.rate_set, None)
        else:
            rates = resources.get('relocation_rate', None)
            if rates is not None: self.rate_set = rates.get_dataset_name()
        if (rates is None) or (not isinstance(rates, RateDataset)):
            logger.log_warning("Rate table %s is not loaded; agents in agent_set %s will have probability of 0.0" % (self.rate_set, self.agent_set))
            return zeros(agents.size(), dtype="float32")

        probability = rates.get_rate(agents)
        return probability

    def get_dependent_datasets(self):
        return [self.agent_set, self.rate_set]