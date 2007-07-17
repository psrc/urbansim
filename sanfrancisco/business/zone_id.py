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
from urbansim.functions import attribute_label

class zone_id(Variable):
    """The taz id of this business. """
   
    def dependencies(self):
        return ["_zone_id=business.disaggregate(parcel.zone_id, intermediates=[building])"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_zone_id")

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'parcel':
            {"parcel_id":array([1,2,3,4,5]),
             "zone_id":  array([2,1,2,3,1]),
             },
            'building':
            {"building_id":array([1,2,3,4,5]),
             "parcel_id":array([1,1,2,3,5])
             },
            'business':
            {"business_id":array([1,2,3,4,5]),
             "building_id":array([1,1,2,3,7])
             },
             
           }
        )
        
        should_be = array([2, 2, 2, 1, -1])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    
#if __name__=='__main__':
#    import unittest
#    from urbansim.variable_test_toolbox import VariableTestToolbox
#    from numarray import array
#    from numarray.ma import allequal
#    from opus_core.resources import Resources    
#    from sanfrancisco.datasets.parcels import ParcelSet    
#    
#    class Tests(unittest.TestCase):
#        variable_name = "sanfrancisco.household.zone_id"
#
#        def test_my_inputs(self):
#            parcel_id = array([1,1,2,3,7])
##            zone_id = array([4, 5, 6])
#
#            resources = Resources({'data':
#                                   {"parcel_id":array([1,2,3,4,5]),
#                                    "zone_id":  array([2,1,2,3,1]),
#                                    },
#                                  })
#            parcels = ParcelSet(resources=resources, in_storage_type="RAM")
#
#            values = VariableTestToolbox().compute_variable(self.variable_name, \
#                {"household":{ \
#                    "parcel_id":parcel_id}, \
#                 "parcel":parcels }, \
#                dataset = "household")
#            should_be = array([2, 2, 1, 2, -1])
#            
#            self.assertEqual(allequal(values, should_be), \
#                             True, msg = "Error in " + self.variable_name)
#
#    unittest.main()