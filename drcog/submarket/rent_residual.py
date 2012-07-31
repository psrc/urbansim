# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_iv_residual import abstract_iv_residual

class rent_residual(abstract_iv_residual):
    """"""
    p = "bayarea.submarket.avg_rent_per_unit_in_submarket"
    iv = "bayarea.submarket.avg_rent_per_unit_in_county"
    filter = "bayarea.submarket.avg_rent_per_unit_in_submarket > 0"


from opus_core.tests import opus_unittest
from numpy import array, arange, newaxis
from numpy.random import uniform, normal, seed
from opus_core.tests.utils.variable_tester import VariableTester
from opus_core.estimate_linear_regression import estimate_linear_regression
from opus_core.resources import Resources

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        seed(1)
        beta = [10, 15]
        n = 20
        z = uniform(0.1, 2, n)
        r = normal(scale=0.01, size=n)
        y = beta[0] + beta[1] * z + r

        resources = Resources({'outcome': y, 'coefficient_names': array(['bz']),
                               "constant_position": array([0])})
        est = estimate_linear_regression().run(z[:, newaxis], resources=resources)['estimators']
        should_be = y - (est[0] + est[1]*z)

        tester = VariableTester(
                __file__,
                package_order=['urbansim_parcel', 'urbansim'],
                test_data={
                'building':
                        {
                            "building_id":        arange(n)+1,
                            "price_per_unit":       y,
                            "avg_price_per_unit_in_zone": z,
                        },
                    })
        #should_be = r

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=0.01)

if __name__=='__main__':
    opus_unittest.main()
