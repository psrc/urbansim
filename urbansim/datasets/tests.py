# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class TestDataset(UrbansimDataset):
    id_name_default = "id"
    in_table_name_default = "test"
    out_table_name_default = "test"
    dataset_name_default = "test"
    
