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

from opus_core.variable import Variable
from variable_functions import my_attribute_label

class has_DDD_units(Variable):
    """Boolean indicating whether the parcel has DDD residential units"""

    residential_units = "residential_units"

    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number

    def dependencies(self):
        return [my_attribute_label(self.residential_units)]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute(self.residential_units) == self.tnumber

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x == True or x == False", values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allequal
    from opus_core.resources import Resources    
    from sanfrancisco.datasets.parcels import ParcelSet
    
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.parcel.has_2_units"

        def test_my_inputs(self):
            residential_units = array([1, 2, 5])
            resources = Resources({'data':
                                   {"parcel_id":array([1,2,3]),
                                    "residential_units":residential_units,
                                    },
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")

            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"parcel":parcels}, 
                dataset = "parcel")
            should_be = array([False, True, False])
            
            self.assertEqual(allequal(values, should_be), \
                             True, msg = "Error in " + self.variable_name)

    unittest.main()