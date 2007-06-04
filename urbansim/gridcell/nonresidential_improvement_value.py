#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class nonresidential_improvement_value(Variable):
    """Sum of the improvement values for this gridcell that are not residential
    (governmental, commercial, and industrial)"""
    
    governmental_improvement_value = "governmental_improvement_value"
    commercial_improvement_value = "commercial_improvement_value"
    industrial_improvement_value = "industrial_improvement_value"

    def dependencies(self):
        return [my_attribute_label(self.governmental_improvement_value), 
                my_attribute_label(self.commercial_improvement_value), 
                my_attribute_label(self.industrial_improvement_value)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.governmental_improvement_value) + \
               self.get_dataset().get_attribute(self.commercial_improvement_value) + \
               self.get_dataset().get_attribute(self.industrial_improvement_value)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        governmental_improvement_value = array([100, 200, 300])
        commercial_improvement_value = array([1000, 400, 0])
        industrial_improvement_value = array([10000000000, 800, 700])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "governmental_improvement_value":governmental_improvement_value, 
                    "commercial_improvement_value":commercial_improvement_value, 
                    "industrial_improvement_value":industrial_improvement_value
                }
            }
        )
        
        should_be = array([10000001100, 1400, 1000])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()