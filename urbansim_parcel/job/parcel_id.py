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
        return ["_parcel_id = job.disaggregate(building.parcel_id)"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_parcel_id")

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
                "job":{
                    "job_id":array([1, 2, 3, 4, 5, 6, 7, 8]),
                    "building_id":array([1, 2, 2, 2, 3, 3, 4, 5]),
                    },
                "building":{
                    "building_id":array([1,2,3,4,5]),
                    "parcel_id":  array([1,1,2,3,4])
                    },
                "parcel":{
                     "parcel_id":array([1,2,3,4]),
                     "zone_id":  array([1,3,2,2]),
                     "parcel_sqft":array([0.1, 0.2, 0.4, 0.3]) * 43560.0,                     
                 },
                "zone":{
                     "zone_id":array([1,2,3]),
                 }             
                 
           }
        )
        
        should_be = array([1, 1, 1, 1, 2, 2, 3, 4])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
    
#if __name__=='__main__':
#    import unittest
#    from urbansim.variable_test_toolbox import VariableTestToolbox
#    from numpy import array
#    from numpy import ma
#    from opus_core.resources import Resources        
#    from urbansim_parcel.datasets.buildings import BuildingSet
#        
#    class Tests(unittest.TestCase):
#        variable_name = "urbansim_parcel.household.parcel_id"
#        
#        def test_my_inputs(self):
#            building_id = array([1,1,2,3,7])
#
#            resources = Resources({'data':
#                                   {"building_id":array([1,2,3,4,5]),
#                                    "parcel_id":  array([2,1,2,3,1]),
#                                    },
#                                  })
#            buildings = BuildingSet(resources=resources, in_storage_type="RAM")
#            
#            values = VariableTestToolbox().compute_variable(self.variable_name, \
#                {"household":{ \
#                    "building_id":building_id}, \
#                 "building":buildings,
#                  }, \
#                dataset = "household")
#            should_be = array([2, 2, 1, 2, -1])
#
#            self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), \
#                             True, msg = "Error in " + self.variable_name)
#
#    unittest.main()