# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class buildings_SSS_space(Variable):
    """sum of buildings sizes of the given type"""

    _return_type = "int32"
    
    size = "building_size"
    id_name = "grid_id"
    
    def __init__(self, type):
        self.is_type = "is_building_type_%s" % type
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("building", self.size), attribute_label("building", self.is_type),
                attribute_label("building", self.id_name)]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        building = dataset_pool.get_dataset('building')
        s = building.get_attribute(self.size) * building.get_attribute(self.is_type)
        return ds.aggregate_over_ids(building.get_attribute(self.id_name), s, "sum")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id":array([1,2,3,4]), 
                    },
                "building":{ 
                    "building_id": array([1,2,3,4,5]),
                    "grid_id":array([4,2,3,2,2]), 
                    "is_building_type_residential": array([0,1,1,1,0]),
                    "building_size": array([24, 60, 12, 5, 30])
                } 
            }
        )

        should_be = array([0, 65, 12, 0])              
        instance_name = "urbansim.gridcell.buildings_residential_space"  
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
