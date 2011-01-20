# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class NeighborhoodDataset(UrbansimDataset):
    """Set of neighborhoods."""

    id_name_default = "neighborhood_id"
    in_table_name_default = "neighborhoods"
    out_table_name_default = "neighborhoods"
    dataset_name = "neighborhood"
