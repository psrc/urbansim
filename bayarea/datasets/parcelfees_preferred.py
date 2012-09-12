# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ParcelfeesPreferredDataset(UrbansimDataset):
    id_name_default = "parcel_id"
    in_table_name_default = "parcelfees_preferred"
    out_table_name_default = "parcelfees_preferred"
    dataset_name = "parcelfees_preferred"