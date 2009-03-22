# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DemolitionCostPerSqftDataset(UrbansimDataset):
    
    id_name_default = "building_type_id"
    in_table_name_default = "demolition_cost_per_sqft"
    out_table_name_default = "demolition_cost_per_sqft"
    dataset_name = "demolition_cost_per_sqft"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
