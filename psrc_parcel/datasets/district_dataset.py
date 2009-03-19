# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DistrictDataset(UrbansimDataset):
    
    id_name_default = "district_id"
    in_table_name_default = "districts"
    out_table_name_default = "districts"
    dataset_name = "district"
    
    def __init__(self, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
