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
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class number_of_businesses(Variable):
    """Number of businesses in a given parcel"""

    _return_type="int32"
    
    def dependencies(self):
        return ["sanfrancisco.business.parcel_id", \
                my_attribute_label("parcel_id")]

    def compute(self,  dataset_pool):
        businesses = dataset_pool.get_dataset("business")
        return self.get_dataset().sum_dataset_over_ids(businesses, constant=1)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("business").size()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy import ma
    from opus_core.resources import Resources
    from sanfrancisco.datasets.parcels import ParcelSet
    
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.parcel.number_of_businesses"
        def test(self):
#            parcel_id = array([1, 2, 3, 4])
            hh_parcel_id = array([1, 2, 3, 4, 2, -1])
            resources = Resources({'data':
                                   {"parcel_id":array([1,2,3,4])},
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")
            
            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"parcel":parcels, \
                 "business":{ \
                     "parcel_id":hh_parcel_id}}, \
                dataset = "parcel")
            should_be = array([1,2,1,1])
            
            self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()