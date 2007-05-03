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

    def dependencies(self):
        return ["psrc_parcel.development_project_proposal.unit_price_expected",
                "psrc_parcel.development_project_proposal.units_proposed",
                "total_revenue = development_project_proposal.units_proposed * development_project_proposal.unit_price_expected",
                "unit_price = development_project_proposal.disaggregate(parcel.unit_price)",
                "existing_units = development_project_proposal.disaggregate(psrc_parcel.parcel.existing_units)",
                "acquisition_cost = development_project_proposal.unit_price * development_project_proposal.existing_units",
                "total_investment = development_project_proposal.acquisition_cost + psrc_parcel.development_project_proposal.demolition_cost + psrc_parcel.development_project_proposal.construction_cost",
                "profit = development_project_proposal.total_revenue - development_project_proposal.total_investment",
            ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        total_investment = proposals.get_attribute("total_investment")
        profit = proposals.get_attribute("profit")
        return ma.filled( profit / ma.masked_where(total_investment==0, total_investment.astype(float32)), 0.0)
 
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
            package_order=['psrc_parcel','urbansim'],
            test_data={
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'construction_cost_per_unit': array([200000, 200, 90, 100000])
            },                
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "land_price":       array([1000,   500,    1000000]),
            },
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4]),
                "unit_price_expected":array([360000, 400000/1500, 400000/2000, 200000/8, 330000/1000, 420000/4000, 
                                                480000/3, 1400000/2, 4600000/8000, 200000000/1000000, 1000000/4]),
                "land_area_occupied":array([100, 50, 20, 200, 200, 80, 600, 1, 2, 70, 0.5]),
                "units_proposed":array([1, 1500, 2000, 8, 1000, 4000, 3, 2, 8000, 1000000, 4]),
                
            }
            }
        )
        
        should_be = array([0.2, 0.14,  1.0,  -0.8,  
                             0.1, 0.05, -0.2, 
                             0.0, 1/3.6, 1.0/4, 1.0/9])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-3)

if __name__=='__main__':
    opus_unittest.main()
    