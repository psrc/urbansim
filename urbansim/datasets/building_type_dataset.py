# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingTypeDataset(UrbansimDataset):
    id_name_default = "building_type_id"
    in_table_name_default = "building_types"
    out_table_name_default = "building_types"
    dataset_name = "building_type"

    def get_code(self, type):
        return self.get_id_attribute()[self.get_attribute("name") == type][0]