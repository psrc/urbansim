# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.gridcell.vacant_industrial_job_space import vacant_industrial_job_space as gc_vacant_industrial_job_space


class vacant_industrial_job_space(Variable):
    """ The industrial_sqft/industrial_sqft_per_job - number_of_industrial_jobs. """ 

    number_of_industrial_jobs = "number_of_industrial_jobs"
    industrial_sqft = "industrial_sqft"
    sqft = "industrial_sqft_per_job"

    def dependencies(self):
        return [my_attribute_label(self.number_of_industrial_jobs), 
                "%s = zone.aggregate(gridcell.industrial_sqft, function=sum)" % self.industrial_sqft, 
                "%s = zone.aggregate(gridcell.industrial_sqft_per_job, function=mean)" % self.sqft]                             

    def compute(self, dataset_pool):
        vacant_job_space = gc_vacant_industrial_job_space()
        vacant_job_space.set_dataset(self.get_dataset())
        return vacant_job_space.compute(dataset_pool)
    


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.vacant_industrial_job_space"

    def test_my_inputs(self):
        number_of_industrial_jobs = array([12, 0, 39, 0])
        industrial_sqft = array([1200, 16, 3900, 15])
        industrial_sqft_per_job = array([20, 3, 30, 0])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "number_of_industrial_jobs":number_of_industrial_jobs, 
                "industrial_sqft":industrial_sqft, 
                "industrial_sqft_per_job":industrial_sqft_per_job}}, 
            dataset = "zone")
        should_be = array([48.0, 5.0, 91.0, 0.0])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()