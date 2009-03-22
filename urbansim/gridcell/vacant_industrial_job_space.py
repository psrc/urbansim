# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import int32
from numpy import ma
from numpy import float32
from opus_core.misc import clip_to_zero_if_needed

class vacant_industrial_job_space(Variable):
    """ The industrial_sqft/industrial_sqft_per_job - number_of_industrial_jobs. """ 

    number_of_industrial_jobs = "number_of_industrial_jobs"
    industrial_sqft = "industrial_sqft"
    sqft = "industrial_sqft_per_job"

    def dependencies(self):
        return [my_attribute_label(self.number_of_industrial_jobs), 
                my_attribute_label(self.industrial_sqft), 
                my_attribute_label(self.sqft)]

    def compute(self, dataset_pool):
        sqft = self.get_dataset().get_attribute(self.sqft)
        num_of_job_spaces = ma.filled(self.get_dataset().get_attribute(self.industrial_sqft)/ 
                    ma.masked_where(sqft == 0, sqft.astype(float32)), 0.0).astype(int32)
        return  clip_to_zero_if_needed(num_of_job_spaces - self.get_dataset().get_attribute(self.number_of_industrial_jobs),
                      'vacant_industrial_job_space')

    def post_check(self, values, dataset_pool):
        sqft = self.get_dataset().get_attribute(self.sqft)
        num_of_job_spaces = ma.filled(self.get_dataset().get_attribute(self.industrial_sqft)/ 
                    ma.masked_where(sqft == 0, sqft.astype(float32)), 0.0).astype(int32)
        global_max = num_of_job_spaces.max()
        self.do_check("x >= 0 and x <= %s" % global_max, values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        number_of_industrial_jobs = array([12, 0, 39, 0])
        industrial_sqft = array([1200, 16, 3900, 15])
        industrial_sqft_per_job = array([20, 3, 30, 0])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "number_of_industrial_jobs":number_of_industrial_jobs, 
                    "industrial_sqft":industrial_sqft, 
                    "industrial_sqft_per_job":industrial_sqft_per_job
                }
            }
        )
        
        should_be = array([48.0, 5.0, 91.0, 0.0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()