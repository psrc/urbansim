# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
from numpy import ma
from numpy import float32

class acquisition_cost(Variable):
    """
    results = ( (unit_price * existing_units - improvement_value) / land_area(parcel_sqft) ) * land_area_to_be_taken
    + improvement_value * is_redevelopment 
    """ 
    _return_type = "float32"
    
    def dependencies(self):
        return ["urbansim_parcel.development_project_proposal.unit_price",
                "urbansim_parcel.development_project_proposal.existing_units",
                "improvement_value=development_project_proposal.disaggregate(urbansim_parcel.parcel.improvement_value)",
                "urbansim_parcel.development_project_proposal.land_area_taken",
                "land_area=development_project_proposal.disaggregate(parcel.parcel_sqft)",
                
                ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        
        unit_price = proposals.get_attribute("unit_price")
        existing_units = proposals.get_attribute("existing_units")
        improvement_value = proposals.get_attribute("improvement_value")
        land_area_taken = proposals.get_attribute("land_area_taken")
        land_area = proposals.get_attribute("land_area")
        
        ## is_redevelopment is optional, if is_redevelopment is not one of proposal attributes, default to 0
        if 'is_redevelopment' in proposals.get_known_attribute_names():
            is_redevelopment = proposals.get_attribute('is_redevelopment')
        else:
            is_redevelopment = 0
        
        results = safe_array_divide( (unit_price * existing_units - improvement_value), land_area) * land_area_taken + improvement_value * is_redevelopment

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
                "proposal_id":array([1,  2,  3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3,  3 ]),
                "template_id":array([1,  2,  3,  4, 2,  3, 4, 1, 2, 3,  4]),
           "is_redevelopment":array([0,  0,  1,  1, 0,  1, 1, 0, 1, 1,  1]),
           "land_area_taken": array([10000, 20000, 10000, 20000,
                                     22680, 45360, 15120, 
                                     45000, 45000, 90000, 9000,  
                                     ]),
                
            },
            
            }
        )
        
        should_be = array([500000, 1000000, 500000, 1000000,
                           175000,  500000, 266666.666, 
                            20000,   80000, 100000,   64000])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-2)

if __name__=='__main__':
    opus_unittest.main()
    