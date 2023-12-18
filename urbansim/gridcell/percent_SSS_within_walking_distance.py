# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class percent_SSS_within_walking_distance(Variable):
    """There is exactly one variable corresponding to each defined development type dynamic_land_use_variables,
    where "?" is the development type group's NAME (e.g. residential, commercial).
    100 * [sum over c in cell.walking_radius of (if c.development_type.dynamic_land_use_variables == N then 1 else 0)] /
    (number of cells within walking distance)"""

    _return_type="float32"
    def __init__(self, group):
        self.group = group
        self.number_of_development_type_group_wwd = \
            "number_of_development_type_group_"+self.group+"_within_walking_distance"
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.number_of_development_type_group_wwd)]

    def compute(self, dataset_pool):
        urbansim_constant = dataset_pool.get_dataset('urbansim_constant')
        return 100.0*self.get_dataset().get_attribute(self.number_of_development_type_group_wwd)/ \
                                             float(urbansim_constant["walking_distance_footprint"].sum())


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs( self ):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'number_of_development_type_group_residential_within_walking_distance': array([3, 5, 1, 0]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        should_be = array([3/5.0*100.0, 
                           5/5.0*100.0, 
                           1/5.0*100.0, 
                           0/5.0*100.0])
        instance_name = "urbansim.gridcell.percent_residential_within_walking_distance"
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()