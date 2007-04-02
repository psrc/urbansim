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
from numpy import where, zeros, bool8

class is_pre_DDD(Variable):
    """Returns a boolean indicating if the parcel was built before 1940"""
    
    def __init__(self, number):
        self.year = number
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("year_built")]

    def compute(self,  dataset_pool):
        year_built = self.get_dataset().get_attribute("year_built")
        results = zeros(year_built.size, type=bool8)
        results[where(year_built<self.year)] = 1
        return results

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x == False or x == True", values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy import ma
    from opus_core.resources import Resources    
    from sanfrancisco.datasets.parcels import ParcelSet
    
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.parcel.is_pre_1940"

        def test_my_inputs(self):
            resources = Resources({'data':
                                   {"parcel_id":array([1,2,3,4,5]),
                                    "year_built":array([1940, 1941, 1930, 1990, 1911])
                                    },
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")
            
            values = VariableTestToolbox().compute_variable(self.variable_name, 
                { "parcel":parcels}, 
                  dataset = "parcel" )
            should_be = array([False, False, True, False, True])

            self.assertEqual(ma.allequal(values, should_be), \
                             True, msg = "Error in " + self.variable_name)

    unittest.main()