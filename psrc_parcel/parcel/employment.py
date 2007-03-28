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

class employment(Variable):
    """employment in a given parcel"""

    _return_type="Int32"
    
    def dependencies(self):
        return ["psrc_parcel.business.parcel_id", 
                "psrc_parcel.business.employees", 
                my_attribute_label("parcel_id")]

    def compute(self,  dataset_pool):
        households = dataset_pool.get_dataset("business")
        return self.get_dataset().sum_dataset_over_ids(households, "employees")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("business").get_attribute("employees").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array, arange
    from numpy.ma import allclose
    from opus_core.resources import Resources
    from psrc_parcel.datasets.parcels import ParcelSet
    from psrc_parcel.datasets.businesses import BusinessSet
        
    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.parcel.employment"
        def test(self):
            resources = Resources({'data':
                                   {"parcel_id":array([1,2,3,4])},
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")

            resources = Resources({'data':
                                   {"business_id":arange(6)+1,
                                    "parcel_id":array([1, 2, 3, 4, 2, -1]),
                                    "employees":  array([2, 1, 1, 3, 4, 1])},
                                  })
            businesses = BusinessSet(resources=resources, in_storage_type="RAM")
            
            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"parcel":parcels, \
                 "business":businesses}, \
                dataset = "parcel")
            should_be = array([2,5,1,3])
            
            self.assertEqual(allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()