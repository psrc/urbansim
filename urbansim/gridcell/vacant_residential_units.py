# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_residential_units(Variable):
    """The residential_units - number_of_households. """
    _return_type="int32"
    number_of_households = "number_of_households"
    residential_units = "residential_units"

    def dependencies(self):
        return [my_attribute_label(self.number_of_households), 
                my_attribute_label(self.residential_units)]

    def compute(self, dataset_pool):
        resunits = self.get_dataset().get_attribute(self.residential_units)
        return clip_to_zero_if_needed(resunits - 
                    self.get_dataset().get_attribute(self.number_of_households),
                                          'vacant_residential_units')

    def post_check(self, values, dataset_pool):
        global_max = self.get_dataset().get_attribute(self.residential_units).max()
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
                    "number_of_households":number_of_households, 
                    "residential_units":residential_units
                }
            }
        )
        
        should_be = array([770, 5000, 0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()