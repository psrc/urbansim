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

from abstract_within_walking_distance import abstract_within_walking_distance

class households_without_children_within_walking_distance(abstract_within_walking_distance):
    """Sum of the number of households without children in each gridcell, 
    for each gridcell within walking distance"""

    dependent_variable = "number_of_households_without_children"
        
    def post_check(self,  values, arguments=None):
        self.do_check("x >= 0", values)

#
# Small test to check whether this variable works.
# 

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def testEugeneLoadAllFromDisk(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'number_of_households_without_children': array([0,1,2,0]),
                },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([1]),
                    'cell_size': array([150])
                }
            }
        )
        
        should_be = array([0,1,2,0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)
        
        # Try again with four neighbors also within walking distance.
        tester2 = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'number_of_households_without_children': array([0,1,2,0]),
                },
                'urbansim_constant':{
                    'walking_distance_circle_radius': array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        should_be2 = array([3,3,6,3])
        tester2.test_is_equal_for_variable_defined_by_this_module(self, should_be2)
            

if __name__=='__main__':
    opus_unittest.main()
