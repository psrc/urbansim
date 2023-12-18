# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class travel_time_hbw_am_drive_alone_to_cbd(Variable):
    """Travel time to the CBD zone whose ID is the 129.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    #TODO: eliminate hard-coded constant.
    cbd_zone = "129"
    variable_name = "travel_time_hbw_am_drive_alone_to_"+cbd_zone
    def dependencies(self):
        return [attribute_label('gridcell', "grid_id"),
                'psrc.gridcell.' + self.variable_name,
                my_attribute_label('grid_id')]

    def compute(self, dataset_pool):
        gcs = dataset_pool.get_dataset('gridcell')
        parcels = self.get_dataset()
        return parcels.get_join_data(gcs, self.variable_name)
