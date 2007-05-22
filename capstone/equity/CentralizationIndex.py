''' Centralization index from Massey & Denton 1988 '''

from numpy import array, arange, hstack, vstack, sum
from numpy import array, sum, float64, zeros, ones
from decimal import *

'''
	Inputs: proportion of minority group members in an area's subdivisions,
			distances from the subdivisions to the city center,
			land area in an area's subdivisions
	Output: Floating-point number representing the index, ranges from -1 to 1
		-1 indicates that minorities all reside far from the city center
		1 indicates minorities are in the center; 0 is uniform distribution	
'''

class CentralizationIndex(object):

	def __init__(self, min_prop, dist, area):
		assert(min_prop.size is area.size)
		assert(dist.size is area.size)
		
		n = area.size
		
		# need to order the units by increasing distance from the city center
		# the ranking in that order is used as the indexing number
		indices = dist.argsort();
		distf = dist[indices].astype(float64)
		areaf = area[indices].astype(float64)
		min_propf = min_prop[indices].astype(float64)
		area_total = areaf.sum()
		area_propf = areaf/area_total
		
		# new vector has cumulative sum of areas for zones between central city and current
		area_cumul = area_propf.cumsum()
		
		# other new vector has culumulative sum of proportions minority
		min_cumul = min_propf.cumsum()
			
		# multiply these together and sum as indicated
		ACE1 = 0
		ACE2 = 0
		for i in xrange(0, n-1):
			ACE1 = ACE1 + min_cumul[i]*area_cumul[i+1]
			ACE2 = ACE2 + min_cumul[i+1]*area_cumul[i]
		self.ACE = ACE1 - ACE2

	# Get methods	   
	def get_index(self):
		return self.ACE
		
from opus_core.tests import opus_unittest

class TestClusteringIndex(opus_unittest.OpusTestCase):

	# Simple test case

	def test_simple(self):
		self.min_prop = array([0.25, 0.25, 0.25, 0.25])
		self.dist = array([0., 1., 2., 3.])
		self.area = array([1., 1., 1., 1.])
		ans = CentralizationIndex(self.min_prop, self.dist, self.area)
		self.assertAlmostEqual(ans.get_index(), 0.0)

	# Test 2

	def test_central(self):
		self.min_prop = array([1., 0., 0., 0.])
		self.dist = array([0., 1., 2., 3.])
		self.area = array([1., 1., 1., 1.])
		ans = CentralizationIndex(self.min_prop, self.dist, self.area)
		self.assertAlmostEqual(ans.get_index(), 0.75)

	# Test 3

	def test_further(self):
		self.min_prop = array([0., 0., 0., 1.])
		self.dist = array([0., 1., 2., 3.])
		self.area = array([1., 1., 1., 1.])
		ans = CentralizationIndex(self.min_prop, self.dist, self.area)
		self.assertAlmostEqual(ans.get_index(), -0.75)



''' Run tests if this is file is not run as part of something larger '''

if __name__ == '__main__':
	opus_unittest.main()
