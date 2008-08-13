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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class fazdistrict_id(Variable):
    """The Forecast Analysis Zone id of this gridcell"""
    
    faz_fazdistrict_id = "fazdistrict_id"
    
    def dependencies(self):
        return [my_attribute_label("zone_id"), 
                 attribute_label("zone", self.faz_fazdistrict_id)]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.faz_fazdistrict_id)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        zone_id = array([2, 1, 3])
        faz_id = array([3,4, 5])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "zone_id":zone_id
                    }, 
                "zone":{ 
                    "zone_id":array([1,2,3]),
                    "faz_id":faz_id
                    }, 
                "faz":{
                    "faz_id":array([1,2,3,4,5,6]),
                    "fazdistrict_id":array([1,1,1,2,2,2])
                }
            }
        )
        
        should_be = array([2,1,2])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()