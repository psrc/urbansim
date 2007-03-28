#
# Opus software. Copyright (C) 1998-2004 University of Washington
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
from numpy import array, reshape, Int32


class business_relocation_probabilities(Probabilities):
    def run(self, utilities=None, resources=None):
        """ Return a 2D probability array obtained from a RateSet. 'resources' must contain 
        an entry 'rate' (a RateSet dataset) and an entry "job" (a JobSet dataset) 
        that is able to provide an attribute 'sector_id'. Otherwise the method
        returns None. 
        """
        rates = resources.get("rate", None)
        if (rates == None) or (not isinstance(rates, RateDataset)):
            return None
        sector_prob = rates.get_attribute("business_relocation_probability")
        
        business = resources.get("business", None)
        if business == None:
            return None
#        rates.make_rates_array_if_not_made()
        probability = array(map(lambda x: sector_prob[rates.get_id_index(x)], \
            business.get_attribute("building_use_id").astype(Int32)))
        return probability
                   
    def get_dependent_datasets(self):
        return ["rate"]