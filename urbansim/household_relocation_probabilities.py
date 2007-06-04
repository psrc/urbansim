#
# Opus software. Copyright (C) 1998-2007 University of Washington
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
from numpy import array


class household_relocation_probabilities(Probabilities):
    def run(self, utilities=None, resources=None):
        """ Return a 2D probability array obtained from a RateDataset. 'resources' must contain
        an entry 'rate' (a RateDataset dataset) and an entry "household" (a HouseholdDataset dataset)
        that is able to provide an attribute 'age_of_head' and 'income'. Otherwise the method
        returns None.
        """
        rates = resources.get("rate", None)
        if (rates == None) or (not isinstance(rates, RateDataset)):
            return None
        households = resources.get("household", None)
        if households == None:
            return None

        rates.make_rates_array_if_not_made()
        probability = array(map(lambda x,y: rates.get_rate_for_household(x,y),
            households.get_attribute("age_of_head"),
            households.get_attribute("income")))
        rates.delete_rates_array() #to save memory
        return probability

    def get_dependent_datasets(self):
        return ["rate"]