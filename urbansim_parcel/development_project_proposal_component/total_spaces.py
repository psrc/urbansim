# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import unique
from .variable_functions import my_attribute_label
from numpy import zeros

class total_spaces(Variable):
    """return proposed spaces (units) according to unit name of the building type of the component
    """

    _return_type="int32"
        
    def dependencies(self):
        return [
                "unit_name=development_project_proposal_component.disaggregate(building_type.unit_name)"
                ]

    def compute(self,  dataset_pool):
        dppc = self.get_dataset()
        results = zeros(dppc.size(), dtype=self._return_type)
        for unit_name in unique(dppc["unit_name"]):
            #should not count parcel_sqft
            if unit_name == "parcel_sqft":continue
            self.add_and_solve_dependencies(["urbansim_parcel.development_project_proposal_component." + unit_name], dataset_pool)
            matched = dppc["unit_name"] == unit_name
            results[matched] = dppc[unit_name][matched].astype(self._return_type)
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
            "development_project_proposal_component":{"proposal_component_id":array([1,2,3,4,5,6,7,8,9,10]),
                                                      "building_type_id":     array([1,2,2,2,1,2,1,3,2,2]),
                                                      "building_sqft":        array([1,0,0,0,1,3,3,1,2,2])*1000,
                                                      "residential_units":    array([0,3,1,2,0,1,0,1,2,4]),
#                        "unit_name":           array(["building_sqft","residential_units","residential_units","residential_units",
#                          'building_sqft',"residential_units","building_sqft", "parcel_sqft", 
#                          "residential_units","residential_units",]),                                                      
                },
           "building_type":{
                        "building_type_id":    array([1, 2, 3]),
                        "unit_name":           array(["building_sqft", "residential_units", "parcel_sqft"]),
                        }                
        }
        )
        
        should_be = array([1000, 3, 1, 2, 1000,  1, 3000, 0, 2, 4])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
