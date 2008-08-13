#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
                "parcel":{                        
                          'parcel_id':array([1,2,3]),
                          "parcel_sqft":array([1000,200,1300]),
                          },
                 "building":{
                        'building_id':     array([1,   2,   3,   4,   5,   6,   7]),
                        'parcel_id':       array([1,   1,   2,   3,   3,   3,   3]),
                        "land_area":       array([600, 400, 100, 300, 150, 400, 400]),
                }
            }
        )
        
        should_be = array([0,100,50])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()