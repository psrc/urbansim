# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class RaceDataset(UrbansimDataset):
    id_name_default = "race_id"
    in_table_name_default = "race_names"
    out_table_name_default = "race_names"
    dataset_name = "race"
    
