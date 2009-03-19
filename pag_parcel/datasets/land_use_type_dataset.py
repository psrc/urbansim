# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import where
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class LandUseTypeDataset(UrbansimDataset):
    id_name_default = "land_use_type_id"
    in_table_name_default = "land_use_types"
    out_table_name_default = "land_use_types"
    dataset_name = "land_use_type"
    
#    def get_code(self, use):
#        return self.get_id_attribute()[where(self.get_attribute("building_use") == use)]