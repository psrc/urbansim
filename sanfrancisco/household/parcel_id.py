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

class parcel_id(Variable):
    """The parcel_id of household."""

    gc_parcel_id = "parcel_id"
    
    def dependencies(self):
        return [my_attribute_label("building_id"), 
                attribute_label("building", "parcel_id")]
        
    def compute(self,  dataset_pool):
        buildings = dataset_pool.get_dataset("building")
        return self.get_dataset().get_join_data(buildings, name="parcel_id")
    
if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allclose
    from opus_core.resources import Resources        
    from sanfrancisco.datasets.buildings import BuildingSet
        
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.household.parcel_id"
        
        def test_my_inputs(self):
            building_id = array([1,1,2,3,7])

            resources = Resources({'data':
                                   {"building_id":array([1,2,3,4,5]),
                                    "parcel_id":  array([2,1,2,3,1]),
                                    },
                                  })
            buildings = BuildingSet(resources=resources, in_storage_type="RAM")
            
            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"household":{ \
                    "building_id":building_id}, \
                 "building":buildings,
                  }, \
                dataset = "household")
            should_be = array([2, 2, 1, 2, -1])

            self.assertEqual(allclose(values, should_be, rtol=1e-7), \
                             True, msg = "Error in " + self.variable_name)

    unittest.main()