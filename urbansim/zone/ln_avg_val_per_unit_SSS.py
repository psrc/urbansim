# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln
from variable_functions import my_attribute_label

class ln_avg_val_per_unit_SSS(Variable):
    """log(avg_val_per_unit_SSS)"""

    _return_type = "float32"
    
    def __init__(self, type):
        self.dep_variable = "avg_val_per_unit_%s" % type
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.dep_variable)]
    
    def compute(self, dataset_pool):
        return ln(self.get_dataset().get_attribute(self.dep_variable))


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.ln_avg_val_per_unit_commercial"

    def test_my_inputs(self):
        avg_value = array([21,22,27,42]) 
        some_gridcell_zone_ids = array([1,2,1,3]) 
        grid_id = array([1,2,3,4])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2, 3]),
                 "avg_val_per_unit_commercial": array([10, 5, 0])}, 
             }, 
            dataset = "zone")
        should_be = ln(array([10, 5, 0]))
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()