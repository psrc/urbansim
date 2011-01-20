# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class generalized_cost_hbw_am_drive_alone_to_cbd(Variable):
    """Travel time to the CBD zone whose ID is the 129.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    cbd_zone = "129"
    variable_name = "generalized_cost_hbw_am_drive_alone_to_"+cbd_zone
    def dependencies(self):
        return [my_attribute_label(self.variable_name)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.variable_name)
