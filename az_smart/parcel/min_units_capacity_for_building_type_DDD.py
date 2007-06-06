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

class min_units_capacity_for_building_type_DDD(Variable):
    """ minimum number of units allowed by development constraints  """

    def __init__(self, id_number):
        Variable.__init__(self)
        self.id_number = id_number

    def dependencies(self):
        return ["development_constraint.",
             my_attribute_label(self.residential_units)]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute(self.residential_units) == self.tnumber

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x == True or x == False", values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy import ma
    from opus_core.resources import Resources    
    from az_smart.datasets.parcels import ParcelSet
    
    class Tests(unittest.TestCase):
        variable_name = "az_smart.parcel.has_2_units"

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
            
            self.assertEqual(ma.allequal(values, should_be), \
                             True, msg = "Error in " + self.variable_name)

    unittest.main()