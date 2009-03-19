# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
      
class gc_ln_access_to_workplace_from_residences(Variable):
    """Looks up the variable with the same name that is in zone.  """
    zn_ln_access_to_workplaces_from_residences = "ln_access_to_workplace_from_residences"
    
    def dependencies(self):
        return [my_attribute_label("zone_id"), 
                attribute_label("zone", self.zn_ln_access_to_workplaces_from_residences)]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.zn_ln_access_to_workplaces_from_residences)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        zone_id = array([1, 1, 3, 2])
        tffjth = array([4.1, 5.3, 6.2])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "zone_id":zone_id
                    }, 
                "zone":{ 
                    "zone_id":array([1,2,3]),
                    "ln_access_to_workplace_from_residences": tffjth
                }
            } 
        )
        
        should_be = array([4.1, 4.1, 6.2, 5.3])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()