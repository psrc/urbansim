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

from opus_core.variable import Variable


class double_area(Variable):
    """
    Double the area, double the fun.
    """ 
    _return_type="Float32"
        
    def dependencies(self):
        return ['az_smart.exlu.area']
        
    def compute(self, dataset_pool):
        values = self.get_dataset().get_attribute('area') * 2
        return values
        

from numarray import array

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test(self):
        tester = VariableTester(
            __file__,
            package_order=['az_smart', 'opus_core'],
            test_data={
                'exlu':{
                    'id': array([1, 2]),
                    'area': array([10, 20]),
                    },
            }
        )
        
        should_be = array([20, 40])
        
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()