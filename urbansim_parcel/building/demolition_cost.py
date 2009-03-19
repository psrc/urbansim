# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import zeros, where

class demolition_cost(Variable):
    """demolition cost for each building """
    _return_type = "int32"
    
    def dependencies(self):
        return [my_attribute_label("building_sqft"), 
                "demolition_cost_per_sqft=building.disaggregate(demolition_cost_per_sqft.demolition_cost_per_sqft)"
                ]
        
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        sqft = buildings.get_attribute("building_sqft")
        demolition_cost_per_sqft = buildings.get_attribute("demolition_cost_per_sqft")
        return sqft * demolition_cost_per_sqft
    
    def post_check(self,  values, dataset_pool=None):
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
            'building':
            {
                'building_id': array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                'building_type_id':array([1, 1, 1, 1, 2, 2, 2, 3, 3, 3]),
                'building_sqft': array([19, 2000, 310, 400, 0, 5000, 300, 45, 79, 200]),
                },           
            "demolition_cost_per_sqft":{
                'building_type_id':  array([1, 2, 3]),
                'demolition_cost_per_sqft':array([200, 100, 300])
            },
           }
        )
        
        should_be = array([19*200, 2000*200, 310*200, 400*200, 0, 5000*100, 300*100, 45*300, 79*300, 200*300])
        
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    