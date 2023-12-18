# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label
from numpy import where, ones

class code_for_price_model_vacant_land(Variable):
    """Returns code according to vacant_land_and_building_types table for gridcells of type vacant land, 
    otherwise some other number."""

    _return_type="int8"
    type = "vacant_land"
    is_type = "has_vacant_land"
        
    def dependencies(self):
        return [my_attribute_label(self.is_type),
                attribute_label("vacant_land_and_building_type", "name")]

    def compute(self, dataset_pool):
        code = dataset_pool.get_dataset('vacant_land_and_building_type').get_code(self.type)
        vl = self.get_dataset().get_attribute(self.is_type)
        return where(vl, code, code-1)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{ 
                    'grid_id':array([1,2,3,4]),
                    'vacant_land_sqft': array([10, 0, 5, 0])
                    },
                'vacant_land_and_building_type':{
                    'building_type_id':array([1,2]), 
                    'name': array(['foo', 'commercial']) # Will automatically add 'vacant_land'
                }
            }
        )
            
        should_be = array([3, 2, 3, 2])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()