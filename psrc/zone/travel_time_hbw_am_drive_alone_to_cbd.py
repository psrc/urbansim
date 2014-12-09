# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import minimum
from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class travel_time_hbw_am_drive_alone_to_cbd(Variable):
    """Minimum travel time to CBD zones.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """

    def dependencies(self):
        return [my_attribute_label("travel_time_hbw_am_drive_alone_to_seattle_cbd"),
                my_attribute_label("travel_time_hbw_am_drive_alone_to_bellevue_cbd")]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return minimum(ds["travel_time_hbw_am_drive_alone_to_seattle_cbd"], 
                       ds["travel_time_hbw_am_drive_alone_to_bellevue_cbd"])
