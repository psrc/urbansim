# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class GenericLandUseTypeDataset(UrbansimDataset):
    id_name_default = "generic_land_use_type_id"
    in_table_name_default = "generic_land_use_types"
    out_table_name_default = "generic_land_use_types"
    dataset_name = "generic_land_use_type"
