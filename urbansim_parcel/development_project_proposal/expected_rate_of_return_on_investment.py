# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

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
from opus_core.datasets.dataset_pool import DatasetPool
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
                'density_type': array(['units_per_acre', 'far', 'far', 'units_per_acre' ]),
#                'construction_cost_per_unit': array([200000, 200, 90, 100000])
            },
            'development_template_component':
            {
                'component_id': array([1, 2, 3, 4, 5, 6]),
                'template_id':  array([1, 2, 2, 3, 3, 4]),
                'percent_building_sqft':      array([100,  80,   20,   50, 50, 100]),
                'building_sqft_per_unit':     array([4000, 400,  1,    1,  1,  1000]),
                ## construction_cost_per_unit is actually construction_cost_per_sqft
                'construction_cost_per_unit': array([50,   20,  20,  80, 100, 100]),
#                'building_type':              array([19,   4,    3,    13, 3,   19]), 
                'is_residential':             array([1,    1,    0,    0,  0,   1]),
#                'construction_cost_per_unit': array([200000, 200, 90, 100000])
            },            
            'building':
            {
                "building_id":       array([1,   2,    3]),
                "building_type_id":  array([1,   2,    3]),
                "building_sqft":     array([500, 1500, 1000000]),
                "parcel_id":         array([1,   2,    3]),
            },
            'demolition_cost_per_sqft':
            {
                "building_type_id":         array([1,   2,    3]),
                "demolition_cost_per_sqft": array([50,   25,  15]),
            },
            
            'parcel':
            {
                "parcel_id":        array([1,        2,         3]),
                "parcel_sqft":      array([20000,  45360,  90000]),
                "unit_price":       array([50,     500,    100000]),
                "existing_units":   array([20000,  1000,        1]),
                "improvement_value":array([0,    150000,    60000]), 
            },
                        
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4]),
                "unit_price_expected":array([560000/2000.0, 400000/1500.0, 400000/2000.0, 200000/3000.0, 330000/1000.0, 420000/4000.0, 
                                                480000/5000.0, 1400000/3050.0, 4600000/8000.0, 200000000/1000000.0, 1000000/3500.0]),
                "is_redevelopment":array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                "units_proposed":array([1, 1500, 2000, 8, 1000, 4000, 3, 2, 8000, 1000000, 4]),
                "building_sqft": array([2000, 1500, 2000, 3000, 1000, 4000, 5000, 3050, 8000, 1000000, 3500]),
                "is_redevelopment":array([0,  0,  1,  1, 0,  1, 1, 0, 1, 1,  1]),
                "land_area_taken": array([10000, 20000, 10000, 20000,
                                          22680, 45360, 15120, 
                                          45000, 45000, 90000, 9000,  
                                          ]),
            },
            'development_project_proposal_component':
            {
                "proposal_component_id":array([1,  2, 3,  4, 5,  6,  7,  8,  9,10,11,12, 13,14,15, 16,  17]),
                "component_id":         array([1,  2, 3,  4, 5,  6,  2,  3,  4, 5, 6, 1,  2, 3, 4,  5,  6]),
                "proposal_id":          array([1,  2, 2,  3, 3,  4,  5,  5,  6, 6, 7, 8,  9, 9, 10, 10, 11]),
                "template_id":          array([1,  2, 2,  3, 3,  4,  2,  2,  3, 3, 4, 1,  2, 2, 3,  3,  4]),
                'is_residential':       array([1,  1, 0,  0, 0,  1,  1,  0,  0, 0, 1, 1,  1, 0, 0,  0,  1]),
                
            }
            
            }
        )
## revenue
#array([560000/2000.0, 400000/1500.0, 400000/2000.0, 200000/3000.0, 330000/1000.0, 420000/4000.0, 
#       480000/5000.0, 1400000/3050.0, 4600000/8000.0, 200000000/1000000.0, 1000000/3500.0]),

## acquisition cost        
#                    array([500000, 1000000, 500000, 1000000,
#                           175000,  500000, 266666.666, 
#                            20000,   80000, 100000,   64000])
## demolition cost
#array([0, 0, 50*500, 50*500, 
#       0, 25*1500, 25*1500,
#       0, 15*1000000, 15*1000000, 15*1000000])       
## construction cost
#array([50*4000, 1500*.8*20+1500*.2*20, 2000*.5*80+2000*.5*100, 8*1000*100, 
#              1000*.8*20+1000*.2*20, 4000*.5*80+4000*.5*100, 3*1000*100,
#              2*4000*50, 8000*.8*20+8000*.2*1*20, 1000000*.5*80+1000000*.5*100, 4*1000*100])  
        should_be = array([[-0.2       , -0.61165049, -0.43262411, -0.89041096,  0.69230769,
                        -0.53203343, -0.20551724,  2.33333333, -0.69816273,  0.90294957,
                        -0.93533368]])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-2)

if __name__=='__main__':
    opus_unittest.main()
    
