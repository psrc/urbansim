# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DevelopmentFilterDataset(UrbansimDataset):
    """Set of development constraints."""

    id_name_default = "filter_id"
    in_table_name_default = "development_filters"
    out_table_name_default = "development_filters"
    dataset_name = "development_filter"
