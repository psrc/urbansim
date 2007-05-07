''' Exposure index from Massey & Denton 1988 '''

from numpy import array, sum, float64

'''
    Inputs: population of group X in an area's subdivisions
            population of group Y in an area's subdivisions
            population of everyone in an area's subdivisions
    Output: Floating-point number representing the interaction index,
               ranges from 0 to 1
'''

class ExposureIndex(object):
    def __init__(self, x_pop, y_pop, t_pop):
        assert(x_pop.size is y_pop.size and y_pop.size is t_pop.size)
        xp = x_pop.astype(float64)
        yp = y_pop.astype(float64)
        
        # Find total population of X for entire area
        total_x = x_pop.sum()

        # Calculate
        self.index = ((xp / total_x) * (yp / t_pop)).sum()

    # Getter methods
    def get_index(self):
        return self.index

from opus_core.tests import opus_unittest

class TestExposureIndex(opus_unittest.OpusTestCase):

    # Test "average" case
    def test_simple(self):
        self.x_pop = array([1, 2, 5, 2, 1])
        self.y_pop = array([12, 12, 12, 11, 10])
        self.t_pop = array([16, 16, 12, 20, 16])
        ans = ExposureIndex(self.x_pop, self.y_pop, self.t_pop)

        self.assertAlmostEqual(ans.get_index(), 0.8159091)

    # Test when exposure of x to y is unpossible
    def test_unexposed(self):
        self.x_pop = array([100, 100, 100, 100, 100])
        self.y_pop = array([0, 0, 0, 0, 0])
        self.t_pop = array([100, 100, 100, 100, 100])
        ans = ExposureIndex(self.x_pop, self.y_pop, self.t_pop)

        self.assertAlmostEqual(ans.get_index(), 0)

    # Test when exposure of x to y is very likely
    def test_very_exposed(self):
        self.x_pop = array([1, 1, 1, 1, 1])
        self.y_pop = array([99, 99, 99, 99, 99])
        self.t_pop = array([100, 100, 100, 100, 100])
        ans = ExposureIndex(self.x_pop, self.y_pop, self.t_pop)

        self.assertAlmostEqual(ans.get_index(), 0.99)

''' Run tests if this is file is not run as part of something larger '''
if __name__ == '__main__':
    opus_unittest.main()
