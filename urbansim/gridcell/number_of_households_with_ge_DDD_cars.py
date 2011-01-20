# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_households_with_ge_DDD_cars(Variable):
    """Sum the number of households for a given gridcell that have greater equal than DDD cars"""
    _return_type="int32"
    
    def __init__(self, number):
        self.tnumber = number
        self.has_cars = "has_ge_%s_cars" % self.tnumber
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("household", self.has_cars),
                    'household.grid_id']

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, self.has_cars)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        gridcell_grid_id = array([1, 2, 3])
        hh_grid_id = array([2, 1, 3, 1])
        cars =       array([0, 1, 3, 1])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id":gridcell_grid_id 
                    }, 
                "household":{ 
                    "household_id":array([1,2,3,4]),
                    "grid_id": hh_grid_id, 
                    "cars": cars
                }
            } 
        )
        
        should_be = array([2, 0, 1])
        instance_name = "urbansim.gridcell.number_of_households_with_ge_1_cars"    
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()