# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingSqftPerJobByZoneGenericLandUseTypeIdDataset(UrbansimDataset):
    """
    """
    in_table_name_default = "building_sqft_per_job_by_zone_generic_land_use_type_id"
    out_table_name_default = "building_sqft_per_job_by_zone_generic_land_use_type_id"
    dataset_name = "building_sqft_per_job_by_zone_generic_land_use_type_id"
    id_name_default = "zone_id"
