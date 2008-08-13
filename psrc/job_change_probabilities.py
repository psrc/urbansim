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

from urbansim.datasets.rates import RateDataset
from opus_core.probabilities import Probabilities
from numpy import array, int32, zeros
from opus_core.misc import unique_values

class job_change_probabilities(Probabilities):
    def run(self, utilities=None, resources=None):
        """ Return a 2D probability array obtained from a RateSet. 'resources' must contain
        an entry 'rate' (a RateSet dataset) and an entry "job" (a JobSet dataset)
        that is able to provide an attribute 'sector_id'. Otherwise the method
        returns None.
        """
        rates = resources.get("rate", None)
        if (rates == None) or (not isinstance(rates, RateDataset)):
            return None
        sector_prob = rates.get_attribute("job_change_probability")

        persons = resources.get("person", None)
        if persons == None:
            return None

        persons.compute_variables("psrc.person.job_sector_id", resources=resources)
        #to handle job_sector_ids not appearing in job_change_rates
        job_sectors = unique_values(persons.get_attribute("job_sector_id"))
        change_sectors = rates.get_id_attribute()
        non_sectors = [sector for sector in job_sectors if sector not in change_sectors]
        add_rates = {rates.get_id_name()[0]:array(non_sectors),
                     "job_change_probability":zeros(len(non_sectors), dtype="int32")}

        rates.add_elements(add_rates, require_all_attributes=False)
        probability = array(map(lambda x: sector_prob[rates.get_id_index(x)],
            persons.get_attribute("job_sector_id").astype(int32)))
        return probability

    def get_dependent_datasets(self):
        return ["rate"]