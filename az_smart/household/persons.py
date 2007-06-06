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

class persons(Variable):
    """number of persons in a given household"""

    _return_type="int32"
    
    def dependencies(self):
        return ["person.household_id", 
                my_attribute_label("household_id")]

    def compute(self,  dataset_pool):
        persons = dataset_pool.get_dataset("person")
        return self.get_dataset().sum_dataset_over_ids(persons, constant=1)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("person").size()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy import ma
    from opus_core.resources import Resources
    from az_smart.datasets.persons import PersonSet
    
    class Tests(unittest.TestCase):
        variable_name = "az_smart.household.persons"
        def test(self):
#            parcel_id = array([1, 2, 3, 4])
            resources = Resources({'data':
                                   {"household_id":array([1,1,1,2,3]),
                                    "person_id":array([1,2,3,1,1])},
                                  })
            persons = PersonSet(resources=resources, in_storage_type="RAM")
            
            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"person":persons, \
                 "household":{ \
                     "household_id":array([1, 2, 3])}}, \
                dataset = "household")
            should_be = array([3,1,1])
            
            self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()