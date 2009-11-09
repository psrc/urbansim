# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_potential_household_movers(Variable):
    """Number of households that should potentially move. Expects attribute 'potential_movers'
    of household set that has 1's for households that should move, otherwise 0's."""
    _return_type="int32"
        
    def dependencies(self):
        return [attribute_label("household", "grid_id"), attribute_label("household", "potential_movers")]

    def compute(self, dataset_pool):
        ds = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(ds, "potential_movers")

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('household').size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test(self):
        zone_id = array([1, 2, 3, 4, 5])
        hh_zone_id = array([1, 2, 3, 4, 2, 2])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":zone_id
                    }, 
                "household":{ 
                    "household_id":array([1,2,3,4,5,6]),
                    "grid_id":hh_zone_id,
                    "potential_movers": array([1,1,0,0,0,1])
                }
            } 
        )
        
        should_be = array([1,2,0,0,0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()