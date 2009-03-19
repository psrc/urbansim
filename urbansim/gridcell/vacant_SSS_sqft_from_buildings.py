# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_SSS_sqft_from_buildings(Variable):
    """ The sqft_of_SSS_buildings - sqft_of_SSS_jobs. """ 
    
    _return_type="float32"
    
    def __init__(self, type):
        self.buildings_sqft_variable = "buildings_%s_sqft" % type
        self.sqft_of_jobs = "sqft_of_%s_jobs" % type
        self.type = type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.buildings_sqft_variable), 
                "urbansim.gridcell.%s" % self.sqft_of_jobs]

    def compute(self, dataset_pool):
        sqft = self.get_dataset().get_attribute(self.buildings_sqft_variable)
        return clip_to_zero_if_needed(sqft - 
                    self.get_dataset().get_attribute(self.sqft_of_jobs), 'vacant_%s_sqft_from_buildings' % self.type)

    def post_check(self, values, dataset_pool):
        global_max = self.get_dataset().get_attribute(self.buildings_sqft_variable).max()
        self.do_check("x >= 0 and x <= %s" % global_max, values)
        

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        sqft_of_commercial_jobs = array([1225, 5000, 7600])
        commercial_sqft = array([1995, 10000, 7500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "sqft_of_commercial_jobs":sqft_of_commercial_jobs, 
                    "buildings_commercial_sqft":commercial_sqft
                }
            }
        )
        
        should_be = array([770, 5000, 0])
        instance_name = "urbansim.gridcell.vacant_commercial_sqft_from_buildings"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

    
if __name__=='__main__':
    opus_unittest.main()