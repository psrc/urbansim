# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class income_and_ln_improvement_value_per_unit(Variable):
    """ ln_residential_improvement_value_per_residential_unit * income"""
    _return_type="float32"
    gc_ln_residential_improvement_value_per_residential_unit = \
     "ln_residential_improvement_value_per_residential_unit"
    hh_income = "income"
    
    def dependencies(self):
        self.dep_var = "zone.aggregate("+ attribute_label("gridcell", 
                                         self.gc_ln_residential_improvement_value_per_residential_unit) + \
                                         ", function=sum)"
        return [self.dep_var,
                attribute_label("household", self.hh_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_income, 
                        self.dep_var)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from math import log
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.income_and_ln_improvement_value_per_unit"

    def test_my_inputs(self):
        ln_residential_improvement_value_per_residential_unit = array([log(10), log(100), 0])
        income = array([1000, 300000, 50000, 0, 10550])
        zone_id = array([1,1,2])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"gridcell":{ 
                "ln_residential_improvement_value_per_residential_unit":ln_residential_improvement_value_per_residential_unit,
                "zone_id": zone_id}, 
              "zone":{
                "zone_id":array([1,2])},    
             "household":{ 
                 "income":income}}, 
            dataset = "household_x_zone")
        should_be = array([[6907.755,0], [2072326.58369,0 ], [345387.763949,0], 
                          [0,0], [72876.81819, 0]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()