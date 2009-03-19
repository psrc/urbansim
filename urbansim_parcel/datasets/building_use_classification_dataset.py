# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import where
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingUseClassificationDataset(UrbansimDataset):
    id_name_default = "class_id"
    in_table_name_default = "building_use_classification"
    out_table_name_default = "building_use_classification"
    dataset_name = "building_use_classification"
    
#    def get_code(self, use):
#        return self.get_id_attribute()[where(self.get_attribute("building_use") == use)]