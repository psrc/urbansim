# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_jobs(Variable):
    """Number of jobs in each area"""
    _return_type="int32"

    def dependencies(self):
        return [attribute_label("faz", "large_area_id"), 
                attribute_label("faz", "number_of_jobs"), 
                my_attribute_label("large_area_id")]

    def compute(self, dataset_pool):
        faz = dataset_pool.get_dataset('faz')
        return self.get_dataset().sum_over_ids(faz.get_attribute("large_area_id"), 
                                   faz.get_attribute("number_of_jobs"))

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('faz').get_attribute("number_of_jobs").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.large_area.number_of_jobs"
 
    def test_my_inputs(self):
        number_of_jobs = array([21,22,27,42]) 
        faz_large_area_ids = array([1,2,1,3]) 
        faz_id = array([1,2,3,4])
            
        values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"large_area":{
                "large_area_id":array([1,2, 3])}, \
            "faz":{ \
                "number_of_jobs":number_of_jobs,\
                "large_area_id":faz_large_area_ids, \
                "faz_id":faz_id}}, \
            dataset = "large_area")

        should_be = array([48, 22, 42])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), \
                         True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()