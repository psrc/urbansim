# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_non_home_based_jobs(Variable):
    """Number of number_of_non_home_based_jobs in the zone."""
    
    _return_type="int32"
    gc_number_of_non_hb_jobs = "number_of_non_home_based_jobs"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_number_of_non_hb_jobs), attribute_label("gridcell", "zone_id")]
    
    def compute(self, dataset_pool):
        return self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('gridcell'), 
                self.gc_number_of_non_hb_jobs)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_non_home_based_jobs"
 
    def test_my_inputs(self):
        number_of_non_home_based_jobs = array([21,22,27,42]) 
        some_gridcell_zone_ids = array([1,2,1,3]) 
        grid_id = array([1,2,3,4])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
                {"zone":{
                "zone_id":array([1,2, 3])}, 
            "gridcell":{ 
                "number_of_non_home_based_jobs":number_of_non_home_based_jobs,
                "zone_id":some_gridcell_zone_ids, 
                "grid_id":grid_id}}, 
            dataset = "zone")
        should_be = array([48, 22, 42])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()