# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_work_access_to_population_DDD(Variable):
    """Bounded natural log of the work_access_to_population for this gridcell"""
    
    _return_type="float32"
      
    def __init__(self, number):
        self.tnumber = number
        self.work_access_to_population = "work_access_to_population_"+str(self.tnumber)
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label(self.work_access_to_population)]
        
    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.work_access_to_population))
        

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from math import log
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        work_access_to_population = array([0.0, 5000.0, 12000.0])
        locations_in_zoneid = array([1, 1, 3, 2, 2])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "zone":{ 
                    "zone_id":array([1,2,3]),
                    "work_access_to_population_2":work_access_to_population
                    }, 
                "gridcell":{ 
                    "grid_id":array([1,2,3,4,5]),
                    "zone_id":locations_in_zoneid
                }
            }
        )
        
        # since we're using bounded log, we get 0.0 for the 0 value of work_access_to_population
        should_be = array([0.0, 0.0, log(12000.0), log(5000.0), log(5000.0)])
        # The number of cars is 2 in this test    
        instance_name = "urbansim.gridcell.ln_work_access_to_population_2"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()
