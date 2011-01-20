# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class sqft_of_SSS_jobs(Variable):
    """Computed by multiplying the number of jobs of the SSS type by the 
    average of sqft per job of the SSS type over all gridcells."""
    _return_type="float32"
    
    def __init__(self, sss):
        Variable.__init__(self)
        self.number_of_jobs = "number_of_%s_jobs" % sss
        self.sqft_per_job = "%s_sqft_per_job" % sss
        
    def dependencies(self):
        return [my_attribute_label(self.number_of_jobs), 
                my_attribute_label(self.sqft_per_job)]

    def compute(self, dataset_pool):
        sqftperjob = self.get_dataset().get_attribute(self.sqft_per_job)
        return self.get_dataset().get_attribute(self.number_of_jobs) * sqftperjob

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array, ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.sqft_of_industrial_jobs"

    def test_my_inputs(self):
        number_of_industrial_jobs = array([0,4,10, 2, 3])
        industrial_sqft_per_job = array([1995, 2005, 2006, 2005, 1000])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "number_of_industrial_jobs":number_of_industrial_jobs,
                "industrial_sqft_per_job":industrial_sqft_per_job}, 
              },
            dataset = "zone")
        should_be = array([0, 8020, 20060, 4010, 3000 ])
        
        self.assertEqual(ma.allclose(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()