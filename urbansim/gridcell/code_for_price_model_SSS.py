# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import where, ones

class code_for_price_model_SSS(Variable):
    """Returns code according to vacant_land_and_building_types table for gridcells of the given type, 
    otherwise some other number."""

    _return_type="int8"

    def __init__(self, type):
        self.has_type = "has_%s_buildings" % type
        self.type = type
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.has_type), 
                attribute_label("building_type", "name")]

    def compute(self, dataset_pool):
        has_buildings = self.get_dataset().get_attribute(self.has_type)
        code = dataset_pool.get_dataset('building_type').get_code(self.type)
        return where(has_buildings, code, code-1)


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
                    'grid_id':array([1,2,3]),
                    },
                'building': {
                    'building_id': array([1,2,3,4,5,6]),
                    'building_type_id': array([1,2,1,2,1,1]),
                    'grid_id': array([2,3,1,1,2,1])
                    },
                'building_type': {
                    'building_type_id':array([1,2]), 
                    'name': array(['foo', 'commercial'])
                }
            }
        )
        
        should_be = array([2, 1, 2])
        instance_name = "urbansim.gridcell.code_for_price_model_commercial"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()