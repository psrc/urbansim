# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class faz_id(Variable):
    """The Forecast Analysis Zone id of this gridcell"""

    zone_faz_id = "faz_id"

    def dependencies(self):
        return [my_attribute_label("zone_id"), attribute_label("zone", self.zone_faz_id)]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.zone_faz_id)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        zone_id = array([2, 1, 3])
        faz_id = array([4, 5, 6])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "zone_id":zone_id
                    },
                "zone":{ 
                    "zone_id":array([1,2,3]),
                    "faz_id":faz_id
                }
            }
        )
        
        should_be = array([5,4,6])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()