# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ParcelDataset(UrbansimDataset):
    
    id_name_default = "parcel_id"
    in_table_name_default = "parcels"
    out_table_name_default = "parcels"
    dataset_name = "parcel"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)