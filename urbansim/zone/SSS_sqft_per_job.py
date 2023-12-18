# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label
from numpy import ma

class SSS_sqft_per_job(Variable):
    """ Aggregation over gridcells """
    
    _return_type = "float32"
    
    def __init__(self, type):
        self.type = type
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("gridcell", "sqft_of_%s_jobs" % self.type), 
                 attribute_label("gridcell", "zone_id"), 
                 my_attribute_label("number_of_%s_jobs" % self.type)]
    
    def compute(self, dataset_pool):
        noj = self.get_dataset().get_attribute("number_of_%s_jobs" % self.type)
        return ma.filled(self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('gridcell'), 
                "sqft_of_%s_jobs" % self.type)/ma.masked_where(noj == 0, noj), 0.0)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.commercial_sqft_per_job"

    def test_my_inputs(self):
        sqft = array([21,22,27,42]) 
        some_gridcell_zone_ids = array([1,2,1,3]) 
        grid_id = array([1,2,3,4])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2, 3]),
                 "number_of_commercial_jobs": array([10, 5, 0])}, 
            "gridcell":{ 
                "sqft_of_commercial_jobs":sqft,
                "zone_id":some_gridcell_zone_ids, 
                "grid_id":grid_id}}, 
            dataset = "zone")
        should_be = array([4.8, 4.4, 0])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()