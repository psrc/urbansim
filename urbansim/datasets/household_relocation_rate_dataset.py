# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from rate_dataset import RateDataset
from numpy import where, int32, zeros, float32

class HouseholdRelocationRateDataset(RateDataset):
    id_name_default = []
    dataset_name = "household_relocation_rate"
    probability_attribute = "probability_of_relocating"
    in_table_name_default = "annual_relocation_rates_for_households"
    out_table_name_default = "annual_relocation_rates_for_households"
    attribute_aliases = {'age':'age_of_head'}
    ## to keep backward compatibility, allow using 'age' for 'age_of_head'
        
from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.storage_factory import StorageFactory
from numpy import array, allclose

class Tests(StochasticTestCase):
    def setUp(self):
        self.prob = array([0.1, 0.4, 0.3, 0.0])
        self.rate_set = self.init_rate_dataset()
        
    def init_rate_dataset(self):
        storage = StorageFactory().get_storage('dict_storage')
        rate_table_name = 'rate'
        storage.write_table(
                table_name=rate_table_name,
                table_data={
                    'age_min':   array([ 0, 0, 31, 31]),
                    'age_max':   array([30, 30,-1, -1]),
                    'income_min':array([ 0, 25, 0, 25]),
                    'income_max':array([24, -1,24, -1]),
                    'probability_of_relocating':self.prob,
                    }
            )

        return HouseholdRelocationRateDataset(in_storage=storage, in_table_name=rate_table_name, what='households')
        
    def tearDown(self):
        del self.prob
        del self.rate_set

    def BLOCK_test_get_rate(self):
        hh = array([[20, 1000], [30, 25000], [60, 0], [99, 30000]])
        expected = array([0.1,             0.4,     0.3,         0.0] )
        results = array([self.rate_set.get_rate(h[0], h[1]) for h in hh])
        
        self.assert_(allclose(results, expected))

    def test_get_rate2(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
                table_name='households',
                table_data={
             'household_id': array([  1,  2,  3,  4]),
                    'age':   array([ 20, 30, 60, 99]),
                    'income':array([  1, 25,  0, 30]),
                    }
        )
        from opus_core.datasets.dataset import Dataset
        hhs = Dataset(in_storage=storage, in_table_name='households', id_name='household_id')
        
        expected = array([0.1,             0.4,     0.3,         0.0] )
        results = self.rate_set.get_rate(hhs)
        
        self.assert_(allclose(results, expected))

    def test_get_rate3(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
                table_name='households',
                table_data={
             'household_id': array([  1,  2,  3,  4]),
              'age_of_head': array([ 20, 30, 60, 99]),
                    'income':array([  1, 25,  0, 30]),
                    }
        )
        from opus_core.datasets.dataset import Dataset
        hhs = Dataset(in_storage=storage, in_table_name='households', id_name='household_id')
        
        expected = array([0.1,             0.4,     0.3,         0.0] )
        results = self.rate_set.get_rate(hhs)
        
        self.assert_(allclose(results, expected))
        
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