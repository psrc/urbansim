# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ZipcodeDataset(UrbansimDataset):
    
    id_name_default = "zip_id"
    in_table_name_default = "zipcodes"
    out_table_name_default = "zipcodes"
    dataset_name = "zipcode"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
