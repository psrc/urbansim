# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class AreaTypeDataset(UrbansimDataset):
    
    id_name_default = "area_type_id"
    in_table_name_default = "area_types"
    out_table_name_default = "area_types"
    dataset_name = "area_type"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
