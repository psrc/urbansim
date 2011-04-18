# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import isnan
from opus_core.variables.variable import Variable
from opus_core.ndimage import mean

class average_household_income(Variable):
    """Computes the average household's income per zone, where missing values are removed from the computation."""
    def dependencies(self):
        return ["household.income", "urbansim_parcel.household.zone_id"]
    
    def compute(self,  dataset_pool):
        zones = self.get_dataset()
        hhs = dataset_pool.get_dataset("household")
        income = hhs["income"]
        valid_income_idx = income > 0
        result = mean(income[valid_income_idx], labels=hhs[zones.get_id_name()[0]][valid_income_idx], 
                        index=zones.get_id_attribute())
        is_nan = isnan(result)
        result[is_nan] = 0
        return result
        
from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
                "household":{
                    "household_id":array([1, 2, 3, 4, 5, 6, 7, 8]),
                    "income": array([200, 300, 0, 50, -1, 0, 10, 60]),
                    "zone_id": array([1,1,1,2,2,4,3,3])
                    },
                "zone":{
                     "zone_id":array([1,2,3,4]),
                 }             
                 
           }
        )
        
        should_be = array([250, 50, 35, 0])

        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
