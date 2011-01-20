# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class number_of_available_non_home_based_jobs(Variable):
    """Number of available non-home-based jobs, as computed by subtracting the current number
    of non-home-based jobs from the total possible number of non-home based jobs."""

    total_number_of_possible_non_home_based_jobs ="total_number_of_possible_non_home_based_jobs"
    number_of_non_home_based_jobs = "number_of_non_home_based_jobs"

    def dependencies(self):
        return [my_attribute_label(self.total_number_of_possible_non_home_based_jobs), 
                my_attribute_label(self.number_of_non_home_based_jobs)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.total_number_of_possible_non_home_based_jobs) - \
                    self.get_dataset().get_attribute(self.number_of_non_home_based_jobs)

    def post_check(self, values, dataset_pool):
        global_max = self.get_dataset().get_attribute(self.total_number_of_possible_non_home_based_jobs).max()
        self.do_check("x >= 0 and x <= %s" % global_max, values)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        total_number_of_possible_non_home_based_jobs = array([0, 1000, 5000, 10000])
        number_of_non_home_based_jobs = array([-500, 500, 1250, 10000])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "total_number_of_possible_non_home_based_jobs":total_number_of_possible_non_home_based_jobs, 
                    "number_of_non_home_based_jobs":number_of_non_home_based_jobs
                }
            }
        )
        
        should_be = array([500, 500.0, 3750.0, 0.0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
