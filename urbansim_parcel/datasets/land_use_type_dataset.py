# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class LandUseTypeDataset(UrbansimDataset):
    id_name_default = "land_use_type_id"
    in_table_name_default = "land_use_types"
    out_table_name_default = "land_use_types"
    dataset_name = "land_use_type"
    
#    def get_code(self, use):
#        return self.get_id_attribute()[where(self.get_attribute("building_use") == use)]