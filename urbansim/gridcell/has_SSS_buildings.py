# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_SSS_buildings(Variable):
    """Returns 1 if the location contains buildings of the given type, otherwise 0."""

    _return_type="bool8"

    def __init__(self, type):
        self.number_of_buildings = "number_of_%s_buildings" % type
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.number_of_buildings)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.number_of_buildings)


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
                    'building_id':      array([1,2,3,4,5,6]),
                    'building_type_id': array([1,2,1,2,1,1]),
                    'grid_id':          array([2,3,1,1,2,1])
                    },
                'building_type': {
                    'building_type_id':array([1,2]), 
                    'name': array(['foo', 'commercial'])
                }
            } 
        )
            
        should_be = array([1, 0, 1])
        instance_name = "urbansim.gridcell.has_commercial_buildings"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()