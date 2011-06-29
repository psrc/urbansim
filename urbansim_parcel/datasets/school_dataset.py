# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class SchoolDataset(UrbansimDataset):
    
    id_name_default = "school_id"
    in_table_name_default = "schools"
    out_table_name_default = "schools"
    dataset_name = "school"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
