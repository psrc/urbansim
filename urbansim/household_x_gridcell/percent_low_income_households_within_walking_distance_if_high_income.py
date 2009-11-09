# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class percent_low_income_households_within_walking_distance_if_high_income(Variable):
    """Percent of huseholds within the walking radius that are designated as low-income, given that the decision-making household is high-income.
    [percent_low_income_households_within_walking_distance if hh.is_high_income is true else 0]"""    
    
    def dependencies(self):
        return [attribute_label("gridcell", "percent_low_income_households_within_walking_distance"), 
                attribute_label("household", "is_high_income")]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            "percent_low_income_households_within_walking_distance",
                                            "is_high_income")     

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_high_income"
    
    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(
            self.variable_name, 
            {"gridcell":{ 
                "percent_low_income_households_within_walking_distance":array([50, 10, 20]),
                }, 
             "household":{ 
                 "is_high_income":array([1, 0, 1, 0]),
                 },
             },
            dataset = "household_x_gridcell")
        should_be = array([[50, 10, 20], [0, 0, 0 ], [50, 10, 20], [0,0,0]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-10), 
                         True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()