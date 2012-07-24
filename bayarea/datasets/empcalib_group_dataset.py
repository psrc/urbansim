# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.subgroup_dataset import SubgroupDataset, generate_unique_ids

class EmpcalibGroupDataset(SubgroupDataset):
    
    id_name_default = 'empcalib_group_id'
    in_table_name_default = "empcalib_group"
    out_table_name_default = "empcalib_group"
    dataset_name = "empcalib_group"
    subgroup_definition = ['bayarea.establishment.county_id', 'establishment.sector_id_new']
    

