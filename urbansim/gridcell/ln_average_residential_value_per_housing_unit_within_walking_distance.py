# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from .variable_functions import my_attribute_label

class ln_average_residential_value_per_housing_unit_within_walking_distance(Variable):
    """Natural log of the average_value_per_housing_unit_within_walking_distance for this gridcell
    ln_bounded((residential_land_value+residential_improvement_value)/residential_units) all within walking distance
    """
    
    _return_type="float32"
    average_value_per_unit_wwd = "average_residential_value_per_housing_unit_within_walking_distance"
     
    def dependencies(self):
        return [my_attribute_label(self.average_value_per_unit_wwd)]
        
    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.average_value_per_unit_wwd))
        
#this is a special case of average_value_per_housing_unit_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft