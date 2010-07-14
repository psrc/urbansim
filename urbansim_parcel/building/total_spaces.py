# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import unique
from variable_functions import my_attribute_label
from numpy import zeros

class total_spaces(Variable):
    """units occupied by consumers, the unit is defined by unit_name in building_types 
       table (either building_sqft or residential_units)
    """

    _return_type="int32"
        
    def dependencies(self):
        return [
                "unit_name=building.disaggregate(building_type.unit_name)"
                ]

    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        results = zeros(buildings.size(), dtype=self._return_type)        
        for unit_name in unique(buildings["unit_name"]):
            #should not count parcel_sqft
            if unit_name == "parcel_sqft":continue
            self.add_and_solve_dependencies(["urbansim_parcel.building." + unit_name], dataset_pool)
            matched = buildings["unit_name"] == unit_name
            results[matched] = buildings[unit_name][matched].astype(self._return_type)
        return results

    def post_check(self,  values, dataset_pool=None):
#        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0")

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            "building":{"building_id":         array([1,2,3,4,5,6,7,8,9,10]),
                        "unit_name":           array(["building_sqft","residential_units","residential_units","residential_units",
                                                      'building_sqft',"residential_units","building_sqft", "parcel_sqft", 
                                                      "residential_units","residential_units",]),
                       "building_sqft":        array([1,0,0,0,1,3,3,1,2,2])*1000,
                       "residential_units":    array([0,3,1,2,0,1,0,1,2,4])
                       #occupied sqft              1400,0,0,0,0,0,1200,0,0,0
                       #occupied units                0,3,3,0,0,1,1, 0,1,1
                },      
        }
        )
        
        should_be = array([1000, 3, 1, 2, 1000,  1, 3000, 0, 2, 4])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()