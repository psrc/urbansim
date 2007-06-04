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
from numpy import array, int32


class employment_relocation_probabilities(Probabilities):
    def run(self, utilities=None, resources=None):
        """ Return a 2D probability array obtained from a RateDataset. 'resources' must contain
        an entry 'rate' (a RateDataset dataset) and an entry "job" (a JobDataset dataset)
        that is able to provide an attribute 'sector_id'. Otherwise the method
        returns None.
        """
        rates = resources.get("rate", None)
        if (rates == None) or (not isinstance(rates, RateDataset)):
            return None
        employment = resources.get("job", None)
        if employment == None:
            return None
        rates.make_rates_array_if_not_made()
        probability = array(map(lambda x: rates.get_rate_for_job(x),
            employment.get_attribute("sector_id").astype(int32)))
        return probability

    def get_dependent_datasets(self):
        return ["rate"]