# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.gridcell.vacant_home_based_job_space import vacant_home_based_job_space as gc_vacant_home_based_job_space


class vacant_home_based_job_space(Variable):
    """For the zone compute how many home-based jobs can be allocated to a zone.
    Assuming one household can have only one home-based job, this variable equals to
    the number of households in a zone minus number of those already having home-based jobs
    """ 

    number_of_home_based_jobs = "number_of_home_based_jobs"
    number_of_households = "number_of_households"

    def dependencies(self):
        return [my_attribute_label(self.number_of_home_based_jobs), 
                 my_attribute_label(self.number_of_households)]

    def compute(self, dataset_pool):
        vacant_job_space = gc_vacant_home_based_job_space()
        vacant_job_space.set_dataset(self.get_dataset())
        return vacant_job_space.compute(dataset_pool)
    


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.vacant_home_based_job_space"

    def test_my_inputs(self):
        number_of_home_based_jobs = array([1225, 5000, 7600])
        number_of_households = array([1995, 10000, 7500])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "number_of_households":number_of_households, 
                "number_of_home_based_jobs":number_of_home_based_jobs}}, 
            dataset = "zone")
            
        should_be = array([770, 5000, 0])
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()