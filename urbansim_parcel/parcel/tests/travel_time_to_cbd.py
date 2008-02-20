#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
                "parcel":{"parcel_id":array([1,2,3,4,5]),
                          "grid_id":array([1, 1, 3, 2, 3])
                        },
                "gridcell":{
                            "grid_id":array([1, 2, 3]),
                            "travel_time_to_cbd":array([100, 1000, 1500]),
                }
            }
        )
        
        should_be = array([100.0, 100.0, 1500.0, 1000.0, 1500.0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)



if __name__=='__main__':
    opus_unittest.main()