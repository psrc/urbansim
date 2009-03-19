# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import sort, where, array

class ConsumptionDataset(UrbansimDataset):
    """Set of consumption data."""

    id_name_default = ["grid_id","billyear","billmonth"]
    in_table_name_default = "WCSR_grid"
    out_table_name_default = "WCSR_grid"
    entity_name_default = "consumption"
    
