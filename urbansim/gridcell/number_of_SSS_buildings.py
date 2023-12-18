# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label

class number_of_SSS_buildings(Variable):
    """Computes the number of buildings of the given type for a gridcell"""

    _return_type="int32"

    def __init__(self, building_type_name):
        self.is_building_type = "is_building_type_%s" % building_type_name
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("building", "grid_id"), 
                attribute_label("building", self.is_building_type)]

    def compute(self, dataset_pool):
        buildings = dataset_pool.get_dataset('building')
        return self.get_dataset().sum_dataset_over_ids(buildings, attribute_name=self.is_building_type)

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('building').size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        gridcell_grid_id = array([1, 2, 3])
        #specify an array of 4 buildings, 1st buildings's grid_id = 2 (it's in gridcell 2), etc.
        b_grid_id = array([2, 1, 3, 1])
        #corresponds to above building array, specifies which buildings in which locations are in the group of interest
        single_family = array([0, 1, 1, 1]) 

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":gridcell_grid_id 
                    }, 
                "building":{ 
                    "building_id":array([1,2,3,4]),
                    "grid_id":b_grid_id, 
                    "is_building_type_single_family":single_family
                }
            } 
        )
        
        should_be = array([2, 0, 1])
        instance_name = "urbansim.gridcell.number_of_single_family_buildings"
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()