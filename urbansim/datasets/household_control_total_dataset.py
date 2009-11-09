# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from control_total_dataset import ControlTotalDataset

class HouseholdControlTotalDataset(ControlTotalDataset):
    id_name_default = []  
    #if both self.id_name_default and id_name argument in __init__ is unspecified, 
    #ControlTotalDataset would use all attributes not beginning with "total"
    #as id_name
    in_table_name_default = "annual_household_control_totals"
    out_table_name_default = "annual_household_control_totals"
    dataset_name = "household_control_total"
    
    def __init__(self, *args, **kwargs):
        ControlTotalDataset.__init__(self, what='household', *args, **kwargs)
