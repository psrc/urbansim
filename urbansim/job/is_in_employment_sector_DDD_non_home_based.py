# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_and, logical_not

class is_in_employment_sector_DDD_non_home_based(Variable):
    """Is the job in employment_sector_DDD and not home_based. """

    nonhome_based = "is_non_home_based_job"
    
    def __init__(self, number):
        self.tnumber = number
        self.is_in_sector = "is_in_employment_sector_" + str(self.tnumber)
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.is_in_sector), 
                my_attribute_label(self.nonhome_based)]
        
    def compute(self, dataset_pool):
        return logical_and(self.get_dataset().get_attribute(self.is_in_sector), 
                           self.get_dataset().get_attribute(self.nonhome_based))

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job.is_in_employment_sector_1_non_home_based"

    def test_my_inputs( self ):
        home_based = array([0, 0, 1, 1])
        sector_id = array([0, 1, 2, 1])

        values = VariableTestToolbox().compute_variable( self.variable_name, 
            {"job":{ 
                "is_home_based_job":home_based, 
                "sector_id":sector_id}}, 
            dataset = "job" )
        should_be = array( [False,True,False,False] )
        
        self.assertEqual( ma.allclose( values, should_be, rtol=1e-7 ), True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()