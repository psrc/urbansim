# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ScreenlineNodeDataset(UrbansimDataset):
    
    id_name_default = ["node_i", "node_j"]
    in_table_name_default = "screenline_nodes"
    out_table_name_default = "screenline_nodes"
    dataset_name = "screenline_node"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
