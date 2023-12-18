# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import array

class is_plan_type_DDD(Variable):
    """Returns a boolean indicating whether this gridcell is 
    of the specified plan type DDD"""

    plan_type_id = "plan_type_id"

    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number

    def dependencies(self):
        return [my_attribute_label(self.plan_type_id)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.plan_type_id) == self.tnumber
        
    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs( self ):
        #declare an array of four locations, each with the specified sector ID below
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1, 2, 3, 4]),
                    "plan_type_id":array([1, 3, 2, 3])
                }
            } 
        )
        
        should_be = array( [False, True, False, True] )
        instance_name = "urbansim.gridcell.is_plan_type_3"    
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()