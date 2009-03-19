# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id": array([1, 2, 3]),
                    "avg_val_per_unit_vacant_land": array([10, 5, 0])
                }
            }
        )
        
        should_be = array([2.3025850929940459, 1.6094379124341003, 0])
        instance_name = 'urbansim.gridcell.ln_avg_val_per_unit_vacant_land'
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
