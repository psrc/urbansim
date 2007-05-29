''' Clustering index from Massey & Denton 1988 '''

from numpy import array, arange, hstack, vstack, sum
from decimal import *
from numpy import exp, sqrt, float64
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

'''
  Inputs: number of minority group members in an area's subdivisions,
      number of majority group members in an area's subdivisions,
      total population in an area's subdivisions,
      distances between centroids of each pair of an area's subdivisions
  Output: Floating-point number representing the index
  Note: number of minority and majority should sum to total; this program is only 
      designed for one minority group
'''
''' TODO: figure out how to get distances between centroids '''

class clustering_index(Variable):

  min_data = "number_of_low_income_households"
  maj_data = "number_of_middle_income_households"
  t_data = "number_of_households"
  dist_data = ""

  def dependencies(self):
    return [attribute_label('gridcell', self.min_data),
            attribute_label('gridcell', self.maj_data),
            attribute_label('gridcell', self.t_data),
            attribute_label('gridcell', self.dist_data)]

  def compute(self, dataset_pool):
    min_num = dataset_pool.get_dataset('gridcell').get_attribute(self.min_data).astype(float64)
    maj_num = dataset_pool.get_dataset('gridcell').get_attribute(self.maj_data).astype(float64)
    total_pop = dataset_pool.get_dataset('gridcell').get_attribute(self.t_data).astype(float64)
    dist = dataset_pool.get_dataset('gridcell').get_attribute(self.dist_data).astype(float64)

    return calc_index(min_num, maj_num, total_pop, dist)

  def calc_index(self, min_num, maj_num, total_pop, dist):
    assert(min_num.size == total_pop.size)
    assert(maj_num.size == total_pop.size)

    X = min_num.sum()
    Y = maj_num.sum()
    T = total_pop.sum()
    Pxx = self.calculate_P(min_num, dist)
    Pyy = self.calculate_P(maj_num, dist)
    Ptt = self.calculate_P(total_pop, dist)
    self.SP = (X*Pxx + Y*Pyy)/(T*Ptt) 

    return self.SP

  # Get methods
  def get_index(self):
    return self.SP

  def calculate_P(self, min_num, dist):
    # Find total population for entire area
    minority = min_num.sum()
    c = exp(-dist)
    n = min_num.size
    # Calculate
    s = 0
    for i in xrange(1, n):
      for j in xrange(1, n):
        s = s + min_num[i] * min_num[j] * c[i][j]
          
    s = s/(minority*minority)
    return s

from opus_core.tests import opus_unittest

class TestClusteringIndex(opus_unittest.OpusTestCase):

  # Simple test case

  def test_simple(self):
    self.min_num = array([15., 15., 15., 15.])
    self.maj_num = array([15., 15., 15., 15.])
    self.total_pop = array([30., 30., 30., 30.])
    self.dist = array([[0, 1, 1, sqrt(2)],
        [1, 0, sqrt(2), 1],
        [1, sqrt(2), 0, 1],
        [sqrt(2), 1, 1, 0]])

    ans = ClusteringIndex(self.min_num, self.maj_num, self.total_pop, self.dist)
    self.assertAlmostEqual(ans.get_index(), 1.0)

  # Test 2

  def test_checkerboard(self):
    self.min_num = array([20., 10., 10., 20.])
    self.maj_num = array([10., 20., 20., 10.])
    self.total_pop = array([30., 30., 30., 30.])
    self.dist = array([[0, 1, 1, sqrt(2)],
        [1, 0, sqrt(2), 1],
        [1, sqrt(2), 0, 1],
        [sqrt(2), 1, 1, 0]])
    ans = ClusteringIndex(self.min_num, self.maj_num, self.total_pop, self.dist)
    self.assertAlmostEqual(ans.get_index(), 1.04515299)

  # Test 3

  def test_enclave(self):
    self.min_num = array([20., 20., 10., 10.])
    self.maj_num = array([10., 10., 20., 20.])
    self.total_pop = array([30., 30., 30., 30.])
    self.dist = array([[0, 1, 1, sqrt(2)],
        [1, 0, sqrt(2), 1],
        [1, sqrt(2), 0, 1],
        [sqrt(2), 1, 1, 0]])

    ans = ClusteringIndex(self.min_num, self.maj_num, self.total_pop, self.dist)
    self.assertAlmostEqual(ans.get_index(), 1.05633751)


''' Run tests if this is file is not run as part of something larger '''

if __name__ == '__main__':
  opus_unittest.main()
