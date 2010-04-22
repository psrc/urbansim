# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class PersonDataset(UrbansimDataset):
    
    id_name_default = ["person_id"]
    in_table_name_default = "persons"
    out_table_name_default = "persons"
    dataset_name = "person"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)