# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label, attribute_label

class ln_access_from_residence_to_workplaces_DDD(Variable):
    """Looks up the variable with the same name that is in zone. """
    def __init__(self, number):
        self.tnumber = number
        self.ln_access_from_residence_to_workplaces_in_zone = "ln_access_from_residence_to_workplaces_%d" % int(self.tnumber)
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("zone_id"), 
                attribute_label("zone", self.ln_access_from_residence_to_workplaces_in_zone)]
                
    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.ln_access_from_residence_to_workplaces_in_zone)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id": array([1, 2, 3]),
                    "zone_id": array([1, 1, 3])
                    },
                "zone":{ 
                    "zone_id": array([1, 2, 3]),
                    "ln_access_from_residence_to_workplaces_2": array([4.1, 5.3, 6.2])
                }
            }
        )
        
        should_be = array([4.1, 4.1, 6.2])
        instance_name = "urbansim.gridcell.ln_access_from_residence_to_workplaces_2"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()