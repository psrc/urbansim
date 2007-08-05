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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class zone_id(Variable):
    """The taz id of this job. """
   
    def dependencies(self):
        return [my_attribute_label("building_id"), "urbansim_parcel.building.zone_id"]
        
    def compute(self,  dataset_pool):
        buildings = dataset_pool.get_dataset("building")
        return self.get_dataset().get_join_data(buildings, name="zone_id")
    
if __name__=='__main__':
    import unittest
    from numpy import array
    from opus_core.tests.utils.variable_tester import VariableTester
    
    class Tests(unittest.TestCase):

        def test_my_inputs(self):
            building_id = array([1,1,2,3,7])
#            zone_id = array([4, 5, 6])

            tester = VariableTester(
                        __file__,
                         package_order =['urbansim_parcel','urbansim'],
                         test_data={'building':
                                               {"building_id":array([1,2,3,4,5]),
                                                "zone_id":  array([2,1,2,3,1]),
                                                },
                                    "job":{ 
                                                 "job_id": array([1,2,3,4,5]),
                                                 "building_id": building_id
                                                 },
                                  })

            should_be = array([2, 2, 1, 2, -1])
            tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

    unittest.main()