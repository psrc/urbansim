# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingUseDataset(UrbansimDataset):
    id_name_default = "building_use_id"
    in_table_name_default = "building_use"
    out_table_name_default = "building_use"
    dataset_name = "building_use"
    
    def get_code(self, use):
        return self.get_id_attribute()[where(self.get_attribute("building_use") == use)]