#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import array, where, int32, zeros, float32, apply_along_axis, reshape, maximum
from numpy.random import normal
from numpy.random import seed

class RateDataset(UrbansimDataset):

    id_name_default = {"households":["age_min","income_min"],
                       "jobs":"sector_id",
                       "business":"sector_id"}
    dataset_name = "rate"
    probability_attribute = {"households": "probability_of_relocating",
                             "jobs": "job_relocation_probability"}

    def __init__(self, resources=None, what="households", **kwargs):
        self.id_name_default = self.id_name_default[what]
        self.in_table_name_default = "annual_relocation_rates_for_" + what
        self.out_table_name_default = self.in_table_name_default
        self.what = what

        UrbansimDataset.__init__(self, resources, **kwargs)

        self.rates = None

    def make_rates_array(self):
        if self.what == "households":
            self.make_rates_array_for_households()
        elif self.what == "jobs":
            self.make_rates_array_for_jobs()
        else:
            raise StandardError, "Method 'make_categories' for " + self.what + " not implemented."

    def is_rates_array_made(self):
        return self.rates <> None

    def make_rates_array_if_not_made(self):
        if not self.is_rates_array_made():
            self.make_rates_array()

    def delete_rates_array(self):
        self.rates=None

    def make_rates_array_for_households(self):
        age_min = self.get_attribute("age_min").astype(int32)
        age_max = self.get_attribute("age_max").astype(int32)
        if age_max.min() < 0:
            maximal_age = age_min.max()
            age_max = where(age_max < 0, maximal_age, age_max)
        else:
            maximal_age = age_max.max()

        income_min = self.get_attribute("income_min")
        income_max = self.get_attribute("income_max")
        income_min_div = (income_min/10).astype(int32)
        income_max_div = (income_max/10).astype(int32)
        if income_max.min() < 0:
            maximum_income = income_min_div.max()
        else:
            maximum_income = income_max_div.max()
        probs = self.get_attribute(self.get_probability_attribute_name())
        self.rates = zeros((maximal_age+1,maximum_income+1), dtype=float32)
        for i in range(self.size()):
            for j in range(age_min[i],(age_max[i]+1)):
                for k in range(income_min_div[i],max(income_max_div[i], income_min_div[i]+1)):
                    self.rates[j,k] = probs[i]

    def make_rates_array_for_jobs(self):
        self.rates = self.get_attribute(self.get_probability_attribute_name())

    def get_rate_for_household(self, age, income):
        return self.rates[int(min(age, self.rates.shape[0]-1)), int(min(income/10, self.rates.shape[1]-1))]

    def get_rate_for_job(self, sector_id):
        return self.rates[self.get_id_index(sector_id)]

    def get_probability_attribute_name(self):
        return self.probability_attribute[self.what]

    def sample_rates(self, n=100, cache_storage=None, multiplicator=1):
        """ Draw a samples from non-zero rates. """
        minimum_sd = 1e-20
        probs = self.get_attribute(self.get_probability_attribute_name())
        non_zero_probs_idx = where(probs > 0)[0]
        non_zero_probs = probs[non_zero_probs_idx]
        sd = non_zero_probs * (1-non_zero_probs)/float(n)
        def draw_rn (mean_var, l):
            return normal(mean_var[0], mean_var[1], size=l)
        sampled_values = reshape(apply_along_axis(draw_rn, 0, (non_zero_probs, maximum(multiplicator*sd, minimum_sd)), 1),
                                 (non_zero_probs.size,))
        probs[non_zero_probs_idx] = sampled_values
        self.add_primary_attribute(name=self.get_probability_attribute_name(), data=probs)
        if cache_storage is not None:
            self.write_dataset(out_storage=cache_storage)

from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.storage_factory import StorageFactory


class Tests(StochasticTestCase):
    def test_sampling_rates(self):
        rates = array([0.1, 0.4, 0.3, 0.0])
        n = 100
        expected_results = rates
        seed(10)

        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            rate_table_name = 'rate'
            storage.write_table(
                    table_name=rate_table_name,
                    table_data={
                        'job_relocation_probability':rates,
                        'sector_id': array([1,2,3,4])
                        }
                )

            rate_set = RateDataset(in_storage=storage, in_table_name=rate_table_name, what='jobs')

            rate_set.sample_rates(n=n)
            result = rate_set.get_attribute('job_relocation_probability')

            return result

        def run_stochastic_test():
            self.compute_stochastic_test_normal(run_model, expected_results, 10, transformation=None)
            return self.variance


        self.run_stochastic_test(__file__, run_model, expected_results, 20, type='normal',
                                 significance_level=0.001)
        expected_variance = array([ 0.0009,  0.0024,  0.0021,  0.])**2.0 # (p*(1-p)/n)^2
        # The variance distribution (chi-squared with n-1 df) is approximated by the normal distr.
        # In this case n (number of replicates) should be more than 15.
        self.run_stochastic_test(__file__, run_stochastic_test, expected_variance, 20, type='normal',
                                 significance_level=0.001)

if __name__=='__main__':
    opus_unittest.main()