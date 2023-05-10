# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ZoneControlHctDataset(UrbansimDataset):
    
    id_name_default = "zone_control_hct_id"
    in_table_name_default = "zone_control_hcts"
    out_table_name_default = "zone_control_hcts"
    dataset_name = "zone_control_hct"
    
    def __init__(self, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
