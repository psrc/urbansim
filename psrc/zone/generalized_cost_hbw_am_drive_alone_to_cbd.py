# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import minimum
from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class generalized_cost_hbw_am_drive_alone_to_cbd(Variable):
    """Travel time to the CBD zones (either seattle or bellevue which ever is closer).
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    def dependencies(self):
        return [my_attribute_label("generalized_cost_hbw_am_drive_alone_to_seattle_cbd"),
                my_attribute_label("generalized_cost_hbw_am_drive_alone_to_bellevue_cbd")]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return minimum(ds["generalized_cost_hbw_am_drive_alone_to_seattle_cbd"],
                       ds["generalized_cost_hbw_am_drive_alone_to_bellevue_cbd"])
                       
