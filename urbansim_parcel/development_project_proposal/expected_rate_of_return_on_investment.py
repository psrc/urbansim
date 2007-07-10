#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FORFOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.variables.variable import Variable
from numpy import ma
from numpy import float32

class expected_rate_of_return_on_investment(Variable):
    """
    results = (sale_price_expected - land_and_existing_building_price - demolishing_cost if any - construction_cost) 
    divided by (land_and_existing_building_price + demolishing_cost if any + construction_cost)
    """ 
    _return_type = "float32"
    
    def dependencies(self):
        return ["urbansim_parcel.development_project_proposal.total_investment",
                "urbansim_parcel.development_project_proposal.profit",
                ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        total_investment = proposals.get_attribute("total_investment")
        profit = proposals.get_attribute("profit")
        results = ma.filled( profit / ma.masked_where(total_investment==0, total_investment.astype(float32)), 0.0)

        # TODO: this is to handle anomalies in the regression outcome
        from numpy import clip, isnan, isinf, where
        results[where(isnan(results))] = 0.0
        results[where(isinf(results))] = 0.0
        results = clip(results, -9, 9)

        return results
    
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    
from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'construction_cost_per_unit': array([200000, 200, 90, 100000])
            },                
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "unit_price":       array([500,   500,    1000000]),
                "existing_units":   array([2,    1,      1])
            },
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4]),
                "unit_price_expected":array([360000, 400000/1500, 400000/2000, 200000/8, 330000/1000, 420000/4000, 
                                                480000/3, 1400000/2, 4600000/8000, 200000000/1000000, 1000000/4]),
                #"land_area_taken":array([100, 50, 20, 200, 200, 80, 600, 1, 2, 70, 0.5]),
                "units_proposed":array([1, 1500, 2000, 8, 1000, 4000, 3, 2, 8000, 1000000, 4]),
                
            }
            }
        )
        
        should_be = array([0.79104478, 0.3255814,  1.20994475,  -0.75031211,  
                             0.64588529, 0.16504854, 0.59733777, 
                             0.000, 0.76923077, 1.1978022, -0.28571429])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-2)

if __name__=='__main__':
    opus_unittest.main()
    