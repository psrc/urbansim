# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import safe_array_divide

class avg_val_per_unit_SSS(Variable):
    """Average land value + improvement value over building units (of given type) in each gridcell"""

    _return_type = "float32"
    
    def __init__(self, type):
        self.type = type
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("total_value_%s" % self.type), 
                my_attribute_label("buildings_%s_space_where_total_value" % self.type)]
    
    def compute(self, dataset_pool):
        nou = self.get_dataset().get_attribute("buildings_%s_space_where_total_value" % self.type)
        return safe_array_divide(self.get_dataset().get_attribute(
                "total_value_%s" % self.type), nou)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.gridcell.avg_val_per_unit_commercial"

    def test_my_inputs(self):
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"gridcell":{
                "grid_id":array([1,2, 3,4 ]),
                 "buildings_commercial_space_where_total_value": array([10, 5, 0, 3]),
                 "total_value_commercial": array([101, 10, 5, 0])}
                 }, 
            dataset = "gridcell")
        should_be = array([10.1, 2, 0, 0])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()