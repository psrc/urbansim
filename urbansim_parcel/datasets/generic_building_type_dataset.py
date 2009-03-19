# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class GenericBuildingTypeDataset(UrbansimDataset):
    id_name_default = "generic_building_type_id"
    in_table_name_default = "generic_building_types"
    out_table_name_default = "generic_building_types"
    dataset_name = "generic_building_type"
