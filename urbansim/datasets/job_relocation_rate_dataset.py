# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .rate_dataset import RateDataset

class JobRelocationRateDataset(RateDataset):

    id_name_default = ["sector_id"]
    dataset_name = "annual_job_relocation_rate"
    ## to make the probability_attribute_name back-ward compatible
    probability_attribute = ["probability_of_relocating", "job_relocation_probability"]
    in_table_name_default = "annual_relocation_rates_for_jobs"
    out_table_name_default = "annual_relocation_rates_for_jobs"

from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.storage_factory import StorageFactory
from numpy import array, allclose

class Tests(StochasticTestCase):
    def setUp(self):
        self.sectors = array([1,2,3,4])
        self.prob = array([0.1, 0.4, 0.3, 0.0])
        self.rate_set = self.init_rate_dataset()
        
    def init_rate_dataset(self):
        storage = StorageFactory().get_storage('dict_storage')
        rate_table_name = 'rate'
        storage.write_table(
                table_name=rate_table_name,
                table_data={
                    'sector_id': self.sectors,
                    'job_relocation_probability':self.prob,
                    }
            )

        return JobRelocationRateDataset(in_storage=storage, in_table_name=rate_table_name, what='jobs')
        
    def tearDown(self):
        del self.prob
        del self.rate_set

    def BLOCK_test_get_rate(self):
        results = array([self.rate_set.get_rate(s) for s in self.sectors])
        self.assertTrue(allclose(results, self.prob))

    def test_get_rate2(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
                table_name='jobs',
                table_data={
                    'job_id': array([  1,  2,  3,  4]),
                 'sector_id': self.sectors,
                    }
        )
        from opus_core.datasets.dataset import Dataset
        jobs = Dataset(in_storage=storage, in_table_name='jobs', id_name='job_id')
        
        results = self.rate_set.get_rate(jobs)
        
        self.assertTrue(allclose(results, self.prob))
        
    def test_sampling_rates(self):
        n = 100
        expected_results = self.prob[0:3] # exclude the last 0
        #seed(10)

        def run_model():
            rate_set = self.init_rate_dataset()
            rate_set.sample_rates(n=n)
            result = rate_set.get_attribute(rate_set.get_probability_attribute_name())
            return result[0:3]

        expected_variance = array([ 0.0009,  0.0024,  0.0021])**2.0 # (p*(1-p)/n)^2
        # Test the variance using Chi^2 hypothesis test with known means. These are the rates themselves.
        self.chi_square_test_with_known_mean(run_model, expected_results, expected_variance, 20, significance_level=0.001)
        
if __name__=='__main__':
    opus_unittest.main()