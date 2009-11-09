# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from numpy import zeros, float32
from numpy import ma

class total_number_of_possible_SSS_jobs(Variable):
    """Computed by dividing the total commercial/industrial sqft. of location by the
    commercial/industrial square feet per job
    """
    _return_type = "int32"
    def __init__(self, type):
        self.sqft ="%s_sqft" % type
        self.sqft_per_job = "%s_sqft_per_job" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.sqft),
                my_attribute_label(self.sqft_per_job)]

    def compute(self, dataset_pool):
        com_sqft = self.get_dataset().get_attribute(self.sqft)
        sqft_per_job = self.get_dataset().get_attribute(self.sqft_per_job)
        possible_jobs = zeros(com_sqft.shape, dtype=self._return_type)
        nonzero_index = sqft_per_job != 0
        possible_jobs[nonzero_index] = (com_sqft[nonzero_index] / \
                               sqft_per_job[nonzero_index].astype(float32)).astype(self._return_type)
        return possible_jobs


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs( self ):
        #declare an array of four locations, each with the specified sector ID below
        commercial_sqft = array([1000, 500, 5000, 233])
        commercial_sqft_per_job = array([20, 0, 100, 33])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id":array([1,2,3,4]),
                    "commercial_sqft":commercial_sqft,
                    "commercial_sqft_per_job":commercial_sqft_per_job
                }
            }
        )

        #notice that the computation code above purposely truncates decimal results,
        #which makes sense because fractions of jobs don't exist
        should_be = array( [50.0, 0.0, 50.0, 7.0] )
        instance_name = "urbansim.gridcell.total_number_of_possible_commercial_jobs"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()