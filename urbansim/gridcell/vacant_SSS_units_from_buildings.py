# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_SSS_units_from_buildings(Variable):
    """ residential_units_from_SSS_buildings - number of households. 
        It doesn't distinguish between households living in different type of residential buildings.
    """ 
    
    _return_type="int32"

    number_of_households = "number_of_households"
    
    def __init__(self, type):
        self.units = "buildings_%s_space" % type
        self.type = type
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.units), 
                "urbansim.gridcell.%s" % self.number_of_households]

    def compute(self, dataset_pool):
        units = self.get_dataset().get_attribute(self.units)
        return clip_to_zero_if_needed(units - 
                    self.get_dataset().get_attribute(self.number_of_households), 'vacant_%s_units_from_buildings' % self.type)

    def post_check(self, values, dataset_pool):
        global_max = self.get_dataset().get_attribute(self.units).max()
        self.do_check("x >= 0 and x <= %s" % global_max, values)
        

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        number_of_households = array([1225, 5000, 7500])
        residential_units = array([1995, 10000, 7500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "number_of_households": number_of_households, 
                    "buildings_residential_space": residential_units
                }
            }
        )
        
        should_be = array([770, 5000, 0])
        instance_name = "urbansim.gridcell.vacant_residential_units_from_buildings"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

    
if __name__=='__main__':
    opus_unittest.main()