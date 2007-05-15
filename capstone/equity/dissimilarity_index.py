''' Dissimilarity index from Massey & Denton 1988 '''

from numpy import array, arange, hstack, vstack, sum, float64
from opus_core.variables.variable import Variable

'''
    Inputs: proportion of minority group in an area's subdivisions,
            total population in an area's subdivisions
    Output: Floating-point number representing the index, ranges from 0 to 1
'''

class dissimilarity_index(Variable):
    def __init__(self, min_pop, total_pop):
        #self.pop_attr = total_pop
        #self.min_pop_attr = min_pop
        self.pop_attr = "population"
        self.min_pop_attr = "number_of_minority_households"
                
    def compute(self, dataset_pool):
        ar_total_pop = dataset_pool.get_dataset('gridcell').get_attribute(self.pop_attr).astype(float64)
        ar_min_prop = dataset_pool.get_dataset('gridcell').get_attribute(self.min_pop_attr).astype(float64) / ar_total_pop.sum()
            return calc_index(ar_min_prop, ar_total_pop)
        
    def calc_index(self, ar_min_prop, ar_total_pop):
        # Make some assertions about what we're operating on
        assert(ar_min_prop.size is ar_total_pop.size)
         # proportions must be between 0 and 1!
         assert(ar_min_prop.max() <= 1 and ar_min_prop.min() >= 0)
             
         # Find total population for entire area
         self.total = ar_total_pop.sum()
         self.minority = (ar_min_prop * ar_total_pop).sum() / self.total

         # Calculate
         n = ar_total_pop * abs(ar_min_prop - self.minority)
         d = 2. * self.total * self.minority * (1. - self.minority)
         self.index = sum(n/d)
         return self.index

     # Override me
     def dependencies(self):
         return [attribute_label("gridcell", self.pop_attr),
                     attribute_label("gridcell", self.min_pop_attr)]
             
     # Getter methods            
     def get_index(self):
         return self.index

     def get_total_population(self):
         return self.total

     def get_total_minority_proportion(self):
         return self.minority


# Tests are broken

from opus_core.tests import opus_unittest

class TestDissimilarityIndex(opus_unittest.OpusTestCase):

	# Simple test case
    def test_simple(self):
        self.min_prop = array([1/16., 2/16., 2/12., 1/20., 5/16.])
        self.total_pop = array([16, 16, 12, 20, 16])
        ans = AbstractDissimilarityIndex(None, None)
        ans.calc_index(self.min_prop, self.total_pop)

        self.assertAlmostEqual(ans.get_index(), 0.3320158103)

    # Test when proportions are all the same
    def test_very_even(self):
        self.min_prop = array([0.5, 0.5, 0.5, 0.5])
        self.total_pop = array([10, 10, 11, 12])
        ans = AbstractDissimilarityIndex(None, None)
        ans.calc_index(self.min_prop, self.total_pop)

        self.assertEqual(ans.get_index(), 0.0)

    # Try to get a relatively high index
    def test_very_segregated(self):
        self.min_prop = array([0, 0.3, 0.6, 0.9])
        self.total_pop = array([87, 27, 19, 5])
        ans = AbstractDissimilarityIndex(None, None)
        ans.calc_index(self.min_prop, self.total_pop)

        self.assertAlmostEqual(ans.get_index(), 0.7631579)

''' Run tests if this is file is not run as part of something larger '''
if __name__ == '__main__':
    opus_unittest.main()
