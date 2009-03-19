# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_employment_within_DDD_minutes_travel_time_hbw_am_drive_alone(Variable):
    """Natural log of employment_within_DDD_minutes_travel_time_hbw_am_drive_alone"""
    
    _return_type="float32"    

    def __init__(self, number):
        self.variable_name = 'employment_within_%s_minutes_travel_time_hbw_am_drive_alone' % number
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label(self.variable_name)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.variable_name))

#this is a special case of commercial_sqft_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft