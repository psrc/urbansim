# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class number_of_non_home_based_jobs(Variable):
    """Number of non-home-based jobs in this gridcell, as computed by
    subtracted the number of home based jobs from total jobs"""

    number_of_jobs = "number_of_jobs"
    number_of_home_based_jobs = "number_of_home_based_jobs"

    def dependencies(self):
        return [my_attribute_label(self.number_of_jobs),
                my_attribute_label(self.number_of_home_based_jobs)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.number_of_jobs) - \
               self.get_dataset().get_attribute(self.number_of_home_based_jobs)

    def post_check(self, values, dataset_pool):
        noj = self.get_dataset().get_attribute(self.number_of_jobs).sum()
        self.do_check("x >= 0 and x <= " + str(noj), values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        number_of_jobs = array([500, 1000, 5000, 10000])
        number_of_home_based_jobs = array([500, 500, 1250, 10000])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "number_of_jobs":number_of_jobs, 
                    "number_of_home_based_jobs":number_of_home_based_jobs
                }
            }
        )
        
        should_be = array([0.0, 500.0, 3750.0, 0.0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()