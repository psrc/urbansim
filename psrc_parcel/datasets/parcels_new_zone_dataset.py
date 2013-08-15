# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ParcelsNewZoneDataset(UrbansimDataset):
    
    id_name_default = "parcel_id"
    in_table_name_default = "parcels_new_zones"
    out_table_name_default = "parcels_new_zones"
    dataset_name = "parcels_new_zone"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
