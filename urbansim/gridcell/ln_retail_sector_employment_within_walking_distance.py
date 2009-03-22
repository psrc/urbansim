# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_retail_sector_employment_within_walking_distance(Variable):
    """Natural log of the retail_sector_employment_within_walking_distance for this gridcell"""
    
    _return_type="float32"    
    retail_sector_employment_within_walking_distance = "retail_sector_employment_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.retail_sector_employment_within_walking_distance)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.retail_sector_employment_within_walking_distance))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        """Log of the amount of commercial space on cell.[ln_bounded(c.retail_sector_employment_within_walking_distance )]
        """
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1, 2, 3]),
                    "retail_sector_employment_within_walking_distance":array([1, 1000, 20])
                }
            } 
        )
        
        should_be = array([0.0, 6.907755, 2.995732])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()