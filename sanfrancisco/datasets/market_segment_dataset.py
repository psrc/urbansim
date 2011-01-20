# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.subgroup_dataset import SubgroupDataset, generate_unique_ids
from numpy import array, allclose 

class MarketSegmentDataset(SubgroupDataset):
    
    id_name_default = 'market_segment_id'
    in_table_name_default = "market_segments"
    out_table_name_default = "market_segments"
    dataset_name = "market_segment"
    subgroup_definition = ['sanfrancisco.person_trip.income_break', 'person_trip.mode_id', 'person_trip.time_period']