# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingTypeClassificationDataset(UrbansimDataset):
    id_name_default = "class_id"
    in_table_name_default = "building_type_classification"
    out_table_name_default = "building_type_classification"
    dataset_name = "building_type_classification"
    
#    def get_code(self, use):
#        return self.get_id_attribute()[where(self.get_attribute("building_use") == use)]