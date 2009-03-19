# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import zeros, where

class building_sqft(Variable):
    """total number of sqft for each building """
    _return_type = "int32"
    
    def dependencies(self):
        return [my_attribute_label("residential_units"), my_attribute_label("non_residential_sqft"),
                my_attribute_label("sqft_per_unit")
                ]
        
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        results = zeros(buildings.size(),dtype=self._return_type)
        residential_units = buildings.get_attribute("residential_units")
        sqft = buildings.get_attribute("non_residential_sqft")
        where_residential = where(residential_units > 0)[0]
        where_sqft = where(sqft > 0)[0]
        results[where_residential] = ((residential_units * \
                                        buildings.get_attribute("sqft_per_unit"))[where_residential]).astype(self._return_type)
        results[where_sqft] = results[where_sqft] + (sqft[where_sqft]).astype(self._return_type)
        return results
    
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
                'residential_units': array([7, 2, 3, 0, 2, 3, 4, 1, 0, 0]),
                'non_residential_sqft': array([19, 2000, 310, 400, 0, 0, 0, 45, 79, 200]),
                'sqft_per_unit': array([0, 0, 0, 0, 10, 15, 50, 0, 0, 0])
                },           
            "building_type":{
                'building_type_id':  array([1, 2, 3]),
                'unit_name':         array(['building_sqft', 'residential_units', 'parcel_sqft'])
            },
           }
        )
        
        should_be = array([19, 2000, 310, 400, 2*10, 3*15, 4*50, 45, 79, 200])
        
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    