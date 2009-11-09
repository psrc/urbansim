# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import where

class buildings_SSS_units(Variable):
    """Sum of residential units from buildings of the given type across gridcells."""

    _return_type="float32"

    def __init__(self, type):
        self.is_type_variable = "is_building_type_%s" % type
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("building", self.is_type_variable), 
                attribute_label("building", "residential_units" ),
                attribute_label("building", "grid_id")]

    def compute(self, dataset_pool):
        buildings = dataset_pool.get_dataset('building')
        units = buildings.get_attribute("residential_units")
        type_units = where(buildings.get_attribute(self.is_type_variable), units, 0)
        ds = self.get_dataset()
        return ds.sum_over_ids(buildings.get_attribute(ds.get_id_name()[0]), type_units)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        """Total number of residential units from single family buildings.
        """
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id':array([1,2,3]), 
                    },
                'building': {
                    'building_id':array([1,2,3,4,5,6]),
                    'building_type_id':array([1,2,1,2,1,1]),
                    'grid_id':array([2,3,1,1,2,1]),
                    'residential_units':array([100, 350, 1000, 0, 430, 95])
                    },
                'building_type': {
                    'building_type_id':array([1,2]), 
                    'name': array(['foo', 'single_family'])
                }
            }
        )
            
        should_be = array([0, 0, 350])
        instance_name = "urbansim.gridcell.buildings_single_family_units"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()