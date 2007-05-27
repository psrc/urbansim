''' Exposure index from Massey & Denton 1988 '''

from numpy import array, sum, float64
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

'''
    Inputs: population of group X in an area's subdivisions
            population of group Y in an area's subdivisions
            population of everyone in an area's subdivisions
    Output: Floating-point number representing the interaction index,
               ranges from 0 to 1
'''

class exposure_index(Variable):
    x_data = "number_of_low_income_households"
    y_data = "number_of_high_income_households"
    t_data = "number_of_households"

    # Example of interaction of minorities against everybody else
    def dependencies(self):
        return [attribute_label("gridcell", "region_id"),
                attribute_label("gridcell", self.x_data),
                attribute_label("gridcell", self.y_data),
                attribute_label("gridcell", self.t_data),]

    def compute(self, dataset_pool):
        x_pop = dataset_pool.get_dataset("gridcell").get_attribute(self.x_data).astype(float64)
        y_pop = dataset_pool.get_dataset("gridcell").get_attribute(self.y_data).astype(float64)
        t_pop = dataset_pool.get_dataset("gridcell").get_attribute(self.t_data).astype(float64)

        return self.calc_index(x_pop, y_pop, t_pop)

    def calc_index(self, x_pop, y_pop, t_pop):
        assert(x_pop.size == y_pop.size and y_pop.size == t_pop.size)
        xp = x_pop.astype(float64)
        yp = y_pop.astype(float64)
        
        # Find total population of X for entire area
        total_x = x_pop.sum()

        # Calculate
        self.index = ((xp / total_x) * (yp / t_pop)).sum()
        return self.index
        
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
        ans = ExposureIndex()
        ans = ans.calc_index(self.x_pop, self.y_pop, self.t_pop)

        self.assertAlmostEqual(ans, 0.8159091)

    # Test when exposure of x to y is unpossible
    def test_unexposed(self):
        self.x_pop = array([100, 100, 100, 100, 100])
        self.y_pop = array([0, 0, 0, 0, 0])
        self.t_pop = array([100, 100, 100, 100, 100])
        ans = ExposureIndex()
        ans = ans.calc_index(self.x_pop, self.y_pop, self.t_pop)

        self.assertAlmostEqual(ans, 0)

    # Test when exposure of x to y is very likely
    def test_very_exposed(self):
        self.x_pop = array([1, 1, 1, 1, 1])
        self.y_pop = array([99, 99, 99, 99, 99])
        self.t_pop = array([100, 100, 100, 100, 100])
        ans = ExposureIndex()
        ans = ans.calc_index(self.x_pop, self.y_pop, self.t_pop)

        self.assertAlmostEqual(ans, 0.99)

''' Run tests if this is file is not run as part of something larger '''
if __name__ == '__main__':
    opus_unittest.main()
