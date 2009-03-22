# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_travel_time_weighted_access_to_employment_hbw_am_drive_alone(Variable):
    """Natural log of employment_within_DDD_minutes_travel_time_hbw_am_drive_alone"""
    
    _return_type="float32"    
    
    def dependencies(self):
        return [my_attribute_label("travel_time_weighted_access_to_employment_hbw_am_drive_alone")]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute("travel_time_weighted_access_to_employment_hbw_am_drive_alone"))

#this is a special case of commercial_sqft_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft