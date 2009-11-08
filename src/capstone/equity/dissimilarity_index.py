''' Dissimilarity index from Massey & Denton 1988 '''

from numpy import array, hstack, vstack, sum, float64
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from urbansim.functions import my_attribute_label

'''
    Inputs: proportion of minority group in an area's subdivisions,
            total population in an area's subdivisions
    Output: Floating-point number representing the index, ranges from 0 to 1
'''

class dissimilarity_index(Variable):

    t_data = "number_of_households"
    m_data = "number_of_minority_households"
                
    def compute(self, dataset_pool):
        total_pop = dataset_pool.get_dataset('gridcell').get_attribute(self.t_data).astype(float64)
        min_prop = dataset_pool.get_dataset('gridcell').get_attribute(self.m_data).astype(float64) / total_pop.sum()
        return self.calc_index(min_prop, total_pop)
        
    def calc_index(self, min_prop, total_pop):
        # Make some assertions about what we're operating on
        assert(min_prop.size == total_pop.size)
        # proportions must be between 0 and 1!
        assert(min_prop.max() <= 1 and min_prop.min() >= 0)
            
        # Find total population for entire area
        self.total = total_pop.sum()
        self.minority = (min_prop * total_pop).sum() / self.total

        # Calculate
        n = total_pop * abs(min_prop - self.minority)
        d = 2. * self.total * self.minority * (1. - self.minority)
        self.index = sum(n/d)
        return self.index

        # Override me
    def dependencies(self):
        return [attribute_label("gridcell", self.t_data),
                attribute_label("gridcell", "region_id"),
                attribute_label("gridcell", self.m_data),
                my_attribute_label("region_id")]
                
        # Getter methods            
    def get_index(self):
        return self.index
   
    def get_total_population(self):
        return self.total
   
    def get_total_minority_proportion(self):
        return self.minority
   
   
   # Tests are broken
   
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.region_dataset import RegionDataset
   
class TestDissimilarityIndex(opus_unittest.OpusTestCase):
   
           # Simple test case
    def test_simple(self):
        self.min_prop = array([1/16., 2/16., 2/12., 1/20., 5/16.])
        self.total_pop = array([16, 16, 12, 20, 16])
        ans = dissimilarity_index()
        ans.calc_index(self.min_prop, self.total_pop)

        self.assertAlmostEqual(ans.get_index(), 0.3320158103)
   
       # Test when proportions are all the same
    def test_very_even(self):
        self.min_prop = array([0.5, 0.5, 0.5, 0.5])
        self.total_pop = array([10, 10, 11, 12])
        ans = dissimilarity_index()
        ans.calc_index(self.min_prop, self.total_pop)

        self.assertEqual(ans.get_index(), 0.0)
   
       # Try to get a relatively high index
    def test_very_segregated(self):
        self.min_prop = array([0, 0.3, 0.6, 0.9])
        self.total_pop = array([87, 27, 19, 5])
        ans = dissimilarity_index()
        ans.calc_index(self.min_prop, self.total_pop)

        self.assertAlmostEqual(ans.get_index(), 0.7631579)

    def test_variable(self):
        min_pop = array([1, 2, 2, 1, 5])
        total_pop = array([16, 16, 12, 20, 16])
        grid_id = array([1, 2, 3, 4, 5])

        values = VariableTestToolbox().compute_variable("urbansim.region.dissimilarity_index",
            {"region":RegionDataset(),
             "gridcell": { "number_of_households":total_pop, "number_of_minority_households":min_pop, "grid_id":grid_id } },
            dataset = "region")
        wanted = array([0.3320158103])
        self.assert_(allclose(wanted, values))

''' Run tests if this is file is not run as part of something larger '''
if __name__ == '__main__':
    opus_unittest.main()
