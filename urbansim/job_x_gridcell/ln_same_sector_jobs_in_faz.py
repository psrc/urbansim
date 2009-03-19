# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_same_sector_jobs_in_faz(Variable):
    """Natural log of the same_sector_jobs_in_faz for this gridcell"""
    
    _return_type="float32"  
    same_sector_jobs_in_faz = "same_sector_jobs_in_faz"
    
    def dependencies(self):
        return [my_attribute_label(self.same_sector_jobs_in_faz)]
        
    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.same_sector_jobs_in_faz))
        
#this is a special case of total_value, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job_x_gridcell.ln_same_sector_jobs_in_faz"

    def test_my_inputs(self):
        sector_id = array([1,4,2,1])
        faz_id = array([1,2, 3, 4])
        gc_faz_id = array([1,2, 3, 4])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"faz":{
                "faz_id":faz_id}, 
             "job":{ 
                "sector_id":sector_id, 
                "faz_id":faz_id}, 
             "gridcell":{ 
                "faz_id":gc_faz_id}}, 
            dataset = "job_x_gridcell")
        should_be = array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],[0, 0, 0, 0]])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()