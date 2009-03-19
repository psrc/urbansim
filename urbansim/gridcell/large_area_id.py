# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class large_area_id(Variable):
    """The large_area id of this gridcell"""

    faz_large_area_id = "large_area_id"

    def dependencies(self):
        return [my_attribute_label("faz_id"), 
                attribute_label("faz", "large_area_id")]

    def compute(self, dataset_pool):
        fazes = dataset_pool.get_dataset('faz')
        return self.get_dataset().get_join_data(fazes, name=self.faz_large_area_id)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        faz_id = array([2, 1, 3])
        large_area_id = array([4, 5, 6])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "faz_id":faz_id
                    }, 
                "faz":{ 
                    "faz_id":array([1,2,3]),
                    "large_area_id":large_area_id
                }
            } 
        )
               
        should_be = array([5,4,6])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()