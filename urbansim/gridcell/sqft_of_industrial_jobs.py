# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class sqft_of_industrial_jobs(Variable):
    """Computed by multiplying the number of industrial jobs by the 
    sqft. per industrial jobs"""
    _return_type="float32"
    number_of_industrial_jobs = "number_of_industrial_jobs"
    industrial_sqft_per_job = "industrial_sqft_per_job"

    def dependencies(self):
        return [my_attribute_label(self.number_of_industrial_jobs), 
                my_attribute_label(self.industrial_sqft_per_job)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.number_of_industrial_jobs) * \
               self.get_dataset().get_attribute(self.industrial_sqft_per_job)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        number_of_industrial_jobs = array([0,4,10])
        industrial_sqft_per_job = array([1995, 2005, 2006])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "number_of_industrial_jobs":number_of_industrial_jobs, 
                    "industrial_sqft_per_job":industrial_sqft_per_job
                }
            } 
        )
        
        should_be = array([0, 8020, 20060])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()