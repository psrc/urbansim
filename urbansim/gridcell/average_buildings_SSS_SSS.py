# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from opus_core.misc import safe_array_divide

class average_buildings_SSS_SSS(Variable):
    """number of building units / number of buildings (of that type)"""

    _return_type = "float32"
    
    def __init__(self, type, unit):
        self.building_units = "buildings_%s_%s" % (type, unit)
        self.number_of_units = "number_of_%s_buildings" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.building_units), my_attribute_label(self.number_of_units)]

    def compute(self, dataset_pool):
        return safe_array_divide(self.get_dataset().get_attribute(self.building_units),
                self.get_dataset().get_attribute(self.number_of_units))

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    instance_name = "urbansim.gridcell.average_buildings_residential_units"

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id": array([1,2,3,4]),
                    "buildings_residential_units": array([5, 23, 5, 0]),
                    "number_of_residential_buildings": array([5,5, 1, 0])
                }
            }
        )
        
        should_be = array([1, 4.6, 5, 0])
        tester.test_is_close_for_family_variable(self, should_be, self.instance_name)

if __name__=='__main__':
    opus_unittest.main()
