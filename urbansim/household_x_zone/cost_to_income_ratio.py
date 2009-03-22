# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class cost_to_income_ratio(Variable):
    """ total_annual_rent /income""" 
    _return_type="float32"
    gc_total_annual_rent = "total_annual_rent"
    hh_income = "income"
    
    def dependencies(self):
        self.dep_var = "zone.aggregate("+ attribute_label("gridcell", self.gc_total_annual_rent) + ", function=sum)"
        return [self.dep_var, 
                attribute_label("household", self.hh_income)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().divide(self.dep_var, self.hh_income)

        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.cost_to_income_ratio"
        
    def test_my_inputs(self):
        total_annual_rent = array([1000, 10000, 100000])
        income = array([1, 20, 500])
        zone_id = array([1,1,2])
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"gridcell":{ 
                "total_annual_rent":total_annual_rent,
                "zone_id": zone_id},
             "zone":{
                "zone_id":array([1,2])},   
             "household":{ 
                "income":income}}, 
            dataset = "household_x_zone")
        should_be = array([[11000, 100000], [550, 5000 ], [22, 200]])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()