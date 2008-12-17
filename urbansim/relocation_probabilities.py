#
# Opus software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from urbansim.datasets.rate_dataset import RateDataset
from opus_core.probabilities import Probabilities
from opus_core.logger import logger
from numpy import array, ones


class relocation_probabilities(Probabilities):
    agent_set = 'household'
    rate_set = 'household_relocation_rate'
    
    def run(self, utilities=None, resources=None):
        """ Return a probability array obtained from a RateDataset. 'resources' must contain
        an entry with name self.rate_set (a RateDataset dataset) and an entry self.agent_set dataset
        that is able to provide attributes defined in rate_set columns. Otherwise the method
        returns equal probability of 0.25.
        """
        
        agents = resources.get(self.agent_set, None)
        if agents == None:
            raise RuntimeError("Unable to get agent set " + self.agent_set)

        rates = resources.get(self.rate_set, None)
        if (rates == None) or (not isinstance(rates, RateDataset)):
            logger.log_warning("%s table is not loaded; agents have equal probability of relocating." % self.rate_set)
            return 0.25 * ones(agents.size(), dtype="float32")

        probability = rates.get_rate(agents)
        return probability

    def get_dependent_datasets(self):
        return [self.agent_set, self.rate_set]