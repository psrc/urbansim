# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class TestDataset(UrbansimDataset):
    id_name_default = "id"
    in_table_name_default = "test"
    out_table_name_default = "test"
    dataset_name_default = "test"
    
