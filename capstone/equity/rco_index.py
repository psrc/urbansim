''' RCO index from Massey & Denton 1988 '''

from numpy import array, sum, float64
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

'''
    Inputs: population of group X in an area's subdivisions
            population of group Y in an area's subdivisions
            population of everyone in an area's subdivisions
            size of an area's subdivisions
    Output: Floating-point number representing the relative concentration,
               ranges from -1 to 1
            -1 means y's concentration exceeds x's, 1 is the converse, and
            0 means they're both equally concentrated
'''

class rco_index(Variable):
    x_data = "number_of_low_income_households"
    y_data = "number_of_high_income_households"
    t_data = "population"
    a_data = "acres_of_land"

    def dependencies(self):
        return [attribute_label("gridcell", self.x_data),
                attribute_label("gridcell", self.y_data),
                attribute_label("gridcell", self.t_data),
                attribute_label("gridcell", self.a_data),

    def compute(self):
        x = dataset_pool.get_dataset().get_attribute(self.x_data).astype(float64)
        y = dataset_pool.get_dataset().get_attribute(self.y_data).astype(float64)
        t = dataset_pool.get_dataset().get_attribute(self.t_data).astype(float64)
        a = dataset_pool.get_dataset().get_attribute(self.a_data).astype(float64)

        return calc_index(x, y, t, a)

    def calc_index(self, x, y, t, a):
        assert(x.size is y.size and y.size is t.size and t.size is a.size)

# Sort by area; rearrange the rest of the arguments
        indices = a.argsort();
        af = a[indices].astype(float64)
        xf = x[indices].astype(float64)
        yf = y[indices].astype(float64)
        tf = t[indices]
        
        # Find total population of X for entire area
        total_x = xf.sum()
        total_y = yf.sum()
        n = af.size
        n1 = None
        n2 = None

        # Find n1. n2. T1, T2
        cs = tf.cumsum()
        for i in xrange(n):
            if(cs[i] >= total_x and n1 is None):
                n1 = i
                T1 = cs[i]
            if(cs[n-1] - cs[i] <= total_x and n2 is None):
                n2 = i
                T2 = cs[n-1] - cs[i-1]
                break
            
        # Calculate
        term1 = sum(xf*af/total_x)
        term2 = sum(yf*af/total_y)
        term3 = sum(tf[0:n1+1]*af[0:n1+1])/T1
        term4 = sum(tf[n2:n]*af[n2:n])/T2

        self.index = (term1/term2-1)/(term3/term4-1)
        return self.index

    # Getter methods
    def get_index(self):
        return self.index

from opus_core.tests import opus_unittest

class TestRCOIndex(opus_unittest.OpusTestCase):

    # Test "average" case
    def test_simple(self):
        self.x_pop = array([1, 1, 2, 1, 3])
        self.y_pop = array([4, 0, 3, 1, 1])
        self.t_pop = array([16, 20, 5, 7, 9])
        self.areas = array([1, 1, 2, 3, 4])
        ans = RCOIndex()
        ans = ans.calc_index(self.x_pop, self.y_pop, self.t_pop, self.areas)

        self.assertAlmostEqual(ans.get_index(), -0.5196078)

''' Run tests if this is file is not run as part of something larger '''
if __name__ == '__main__':
    opus_unittest.main()
