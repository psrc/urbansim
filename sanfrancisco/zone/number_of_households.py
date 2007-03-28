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

class number_of_households(Variable):
    """Number of households in a given zone"""

    _return_type="Int32"
    
    def dependencies(self):
        return ["sanfrancisco.parcel.zone_id", 
                "sanfrancisco.parcel.number_of_households", 
                my_attribute_label("zone_id")]

    def compute(self,  dataset_pool):
        parcels = dataset_pool.get_dataset("parcel")
        return self.get_dataset().sum_dataset_over_ids(parcels, "number_of_households")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("parcel").get_attribute("number_of_households").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy.ma import allclose
    from opus_core.resources import Resources
    from sanfrancisco.datasets.parcels import ParcelSet
    
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.zone.number_of_households"
        def test(self):
            resources = Resources({'data':
                                   {"parcel_id": array([1,2,3,4,5,6]),
                                    "number_of_households":array([0,1,4,0,2,5]),
                                    "zone_id":   array([4,1,3,2,1,2])
                                    },
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")

            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"zone":{
                     "zone_id":array([1,2,3,4])}, \
                 "parcel":parcels}, \
                dataset = "zone")
            should_be = array([3,5,4,0])
            
            self.assertEqual(allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()