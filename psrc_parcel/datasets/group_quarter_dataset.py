# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class GroupQuarterDataset(UrbansimDataset):
    
    id_name_default = ["taz", "year"]
    in_table_name_default = "group_quarters"
    out_table_name_default = "group_quarters"
    dataset_name = "group_quarter"
    
    def __init__(self, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
