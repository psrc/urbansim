# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class number_of_households_without_children(Variable):

    _return_type="int32"
    is_without_children = "is_without_children"

    def dependencies(self):
        return [attribute_label("household", self.is_without_children), 
                attribute_label("household", "grid_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, self.is_without_children)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        """Number of homes without children for a given gridcell """
        gridcell_grid_id = array([1, 2, 3])
        #specify an array of 4 households, 1st hh's grid_id = 2 (it's in gridcell 2), etc.
        household_grid_id = array([2, 1, 3, 1] )
        #corresponds to above hh array, specifies which hh's in which locations "qualify"
        is_without_children = array([0, 1, 1, 1] )

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id":gridcell_grid_id 
                    }, 
                "household":{ 
                    "household_id":array([1,2,3,4]),
                    "grid_id":household_grid_id, 
                    "is_without_children":is_without_children
                }
            } 
        )
        
        should_be = array([2, 0, 1])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()