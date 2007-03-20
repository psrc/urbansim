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
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class residential_units(Variable):
    """residential units in a given parcel"""

    _return_type="Int32"
    
    def dependencies(self):
        return [attribute_label("building", "residential_units"), \
                attribute_label("building", "parcel_id"), \
                my_attribute_label("parcel_id")]

    def compute(self,  dataset_pool):
        buildings = dataset_pool.get_dataset("building")
        return self.get_dataset().sum_dataset_over_ids(buildings, "residential_units")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").get_attribute("residential_units").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allclose
    from opus_core.resources import Resources
    from sanfrancisco.datasets.parcels import ParcelSet
    from sanfrancisco.datasets.buildings import BuildingSet
    
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.parcel.residential_units"
        def test(self):
            parcel_resources = Resources({'data':
                                   {"parcel_id":array([1,2,3])},
                                  })
            parcels = ParcelSet(resources=parcel_resources, in_storage_type="RAM")
            building_resources = Resources({'data':
                                   {"building_id":array([1,2,3,4]),
                                    "parcel_id":array([1,2,3,2]),
                                    "residential_units":array([0,1,5,3]),
                                    },
                                  })
            buildings = BuildingSet(resources=building_resources, in_storage_type="RAM")
            
            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"parcel":parcels, \
                 "building":buildings}, \
                dataset = "parcel")
            should_be = array([0,4,5])
            
            self.assertEqual(allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()