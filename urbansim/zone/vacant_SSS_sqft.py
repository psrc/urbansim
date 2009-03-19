# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_SSS_sqft(Variable):
    """ total sqft - sqft_of_jobs of the sss type. """
    _return_type="float32"

    def __init__(self, sss):
        Variable.__init__(self)
        self.type = sss
        self.sqft_of_jobs = "sqft_of_%s_jobs" % self.type
        self.total_sqft = "%s_sqft" % self.type
        
    def dependencies(self):
        return [my_attribute_label(self.sqft_of_jobs), 
                my_attribute_label(self.total_sqft)]

    def compute(self, dataset_pool):
        sqft = self.get_dataset().get_attribute(self.total_sqft)
        return clip_to_zero_if_needed(sqft - 
                    self.get_dataset().get_attribute(self.sqft_of_jobs),
                                          'vacant_%s_sqft' % self.type)
   
    def post_check(self, values, dataset_pool):
        global_max = self.get_dataset().get_attribute(self.total_sqft).max()
        self.do_check("x >= 0 and x <= %s" % global_max, values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.vacant_industrial_sqft"

    def test_my_inputs(self):
        sqft_of_industrial_jobs = array([1225, 5000, 7500])
        industrial_sqft = array([1995, 10000, 7500])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "sqft_of_industrial_jobs":sqft_of_industrial_jobs, 
                "industrial_sqft":industrial_sqft}}, 
            dataset = "zone")
        should_be = array([770, 5000, 0])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()