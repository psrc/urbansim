# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_households(Variable):
    _return_type="int32"

    def dependencies(self):
        return [attribute_label("household", "neighborhood_id")]
 
    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, constant=1)
    
    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('household').size()
        self.do_check("x >= 0 and x <= " + str(size), values)    
        
# This is experimental code
#if __name__=='__main__':
#    from opus_core.tests import opus_unittest
#    from urbansim.variable_test_toolbox import VariableTestToolbox
#    from numpy import array
#    from numpy import ma
#    class Tests(opus_unittest.OpusTestCase):
#        variable_name = "number_of_households"
#        def test(self):
#            """
#            """
#            neighborhood_id = array([1, 2, 3, 4])
#            hh_neighborhood_id = array([1, 2, 3, 4, 2, 2])
#            
#            values = VariableTestToolbox().compute_variable(self.variable_name, \
#                {"neighborhood":{ \
#                    "neighborhood_id":neighborhood_id}, \
#                 "household":{ \
#                    "neighborhood_id":hh_neighborhood_id}}, \
#                dataset = "neighborhood")
#                                                            
#            should_be = array([1,3,1,1])
#            
#            self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
#                             True, msg = "Error in " + self.variable_name)
#    opus_unittest.main()