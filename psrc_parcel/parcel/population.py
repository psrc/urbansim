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

class population(Variable):
    """Number of households in a given parcel"""

    _return_type="Int32"
    
    def dependencies(self):
        return ["psrc_parcel.building.parcel_id", 
                "psrc_parcel.building.population", 
                my_attribute_label("parcel_id")]

    def compute(self,  dataset_pool):
        buildings = dataset_pool.get_dataset("building")
        return self.get_dataset().sum_dataset_over_ids(buildings, "population")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").get_attribute("population").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allclose
    from opus_core.resources import Resources
    from psrc_parcel.datasets.parcels import ParcelSet
    from psrc_parcel.datasets.buildings import BuildingSet
        
    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.parcel.population"
        def test(self):

            resources = Resources({'data':
                                   {"parcel_id":array([1,2,3,4])},
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")
            
            resources = Resources({'data':
                                   {"building_id": array([1,2,3,4,5,6]),
                                    "population":array([0,1,4,0,2,5]),
                                    "parcel_id":   array([4,1,3,2,1,2])
                                    },
                                  })
            buildings = BuildingSet(resources=resources, in_storage_type="RAM")

            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"building":buildings, \
                 "parcel":parcels}, \
                dataset = "parcel")
            should_be = array([3,5,4,0])
            
            self.assertEqual(allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()