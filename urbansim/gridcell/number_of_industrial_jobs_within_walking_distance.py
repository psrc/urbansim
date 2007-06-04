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

class number_of_industrial_jobs_within_walking_distance(abstract_within_walking_distance):
    """Total number of industrial_jobs within walking distance of a given gridcell"""

    dependent_variable = "number_of_industrial_jobs"

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
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'number_of_industrial_jobs': array([20, 0, 100, 1]),
                    },
                'urbansim_constant':{
                    'walking_distance_circle_radius': array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        should_be = array([160, 21, 321, 103])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()