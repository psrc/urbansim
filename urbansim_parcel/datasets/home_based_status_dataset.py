# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class HomeBasedStatusDataset(UrbansimDataset):
    
    id_name_default = "home_based_status"
    in_table_name_default = "home_based_status"
    out_table_name_default = "home_based_status"
    dataset_name = "home_based_status"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
