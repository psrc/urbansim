# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.building_type_dataset import BuildingTypeDataset

class JobBuildingTypeDataset(BuildingTypeDataset):
    id_name_default = "id"
    in_table_name_default = "job_building_types"
    out_table_name_default = "job_building_types"
    dataset_name = "job_building_type"
    
