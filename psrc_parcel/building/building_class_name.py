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

class building_class_name(Variable):
    """The class name (residential, nonresidential) of this building. """
   
    def dependencies(self):
        return [my_attribute_label("building_class_id"), 
                attribute_label("building_use_classification", "class_id"),
                attribute_label("building_use_classification", "name"),
                ]
        
    def compute(self,  dataset_pool):
        building_class = dataset_pool.get_dataset("building_use_classification")
        
        return self.get_dataset().get_join_data(building_class, join_attribute='building_class_id',
                                                name="class_name")
    
#if __name__=='__main__':
#    import unittest
#    from urbansim.variable_test_toolbox import VariableTestToolbox
#    from numarray import array
#    from numarray.ma import allequal
#    from opus_core.resources import Resources    
#    from psrc_parcel.datasets.parcels import ParcelSet    
#    
#    class Tests(unittest.TestCase):
#        variable_name = "psrc_parcel.household.zone_id"
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