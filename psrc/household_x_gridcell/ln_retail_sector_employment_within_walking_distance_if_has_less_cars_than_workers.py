# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class ln_retail_sector_employment_within_walking_distance_if_has_less_cars_than_workers(Variable):
    """Ln Retail employment within walking distance if the household has less cars than workers.
    [retail_employment_within_walking_distance if hh.has_less_cars_than_workers is true else 0]"""    
    
    rew = "ln_retail_sector_employment_within_walking_distance"
    hh_has_less_cars_than_workers = "has_less_cars_than_workers"
        
    def dependencies(self):
        return [attribute_label("household", self.hh_has_less_cars_than_workers),
                attribute_label("gridcell", self.rew)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(self.rew, 
                                                                    self.hh_has_less_cars_than_workers)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.opus_package_info import package

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_gridcell.ln_retail_sector_employment_within_walking_distance_if_has_less_cars_than_workers"
    
    def test_my_inputs(self):
        ln_retail_sector_employment_within_walking_distance = array([50, 0, 15])
        has_less_cars_than_workers = array([1, 0, 1, 1])
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"gridcell":{ \
                 "ln_retail_sector_employment_within_walking_distance":ln_retail_sector_employment_within_walking_distance}, \
             "household":{ \
                 "has_less_cars_than_workers":has_less_cars_than_workers}}, \
            dataset = "household_x_gridcell")
        should_be = array([[50, 0, 15], [0, 0, 0], [50, 0, 15], [50, 0, 15]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-10), \
                         True, msg = "Error in " + self.variable_name)
                        
                         
if __name__=='__main__':
    opus_unittest.main()