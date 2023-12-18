# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import clip_to_zero_if_needed
from .variable_functions import my_attribute_label

class vacant_SSS_job_space_from_buildings(Variable):
    """ The SSS_sqft_from_buildings/SSS_sqft_per_job - number_of_SSS_jobs. """ 

    _return_type = "int32"
    
    def __init__(self, type):
        self.number_of_jobs = "number_of_%s_jobs" % type
        self.possible_jobs = "total_number_of_possible_%s_jobs_from_buildings" % type
        self.variable_name = "vacant_%s_job_space_from_buildings" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.number_of_jobs), 
                my_attribute_label(self.possible_jobs)]                             

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return  clip_to_zero_if_needed(ds.get_attribute(self.possible_jobs) - 
                    ds.get_attribute(self.number_of_jobs), self.variable_name)
    


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        number_of_commercial_jobs = array([12, 39, 0, 10])
        commercial_sqft = array([1205, 16, 3900, 15])
        commercial_sqft_per_job = array([20, 3, 30, 0])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "number_of_commercial_jobs":number_of_commercial_jobs,
                    "buildings_commercial_sqft":commercial_sqft, 
                    "commercial_sqft_per_job":commercial_sqft_per_job
                }
            }
        )
    
        should_be = array([60 - 12, 0, 3900/30, 0])
        instance_name = "urbansim.gridcell.vacant_commercial_job_space_from_buildings"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()