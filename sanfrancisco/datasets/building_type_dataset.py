# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingTypeDataset(UrbansimDataset):
    id_name_default = "building_type_id"
    in_table_name_default = "building_types"
    out_table_name_default = "building_types"
    dataset_name = "building_type"
    
    def get_code(self, type_id):
        return self.get_id_attribute()[where(self.get_attribute("building_type_id") == type_id)]