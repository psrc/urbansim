# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import sort, where, array

class ConsumptionDataset(UrbansimDataset):
    """Set of consumption data."""

    id_name_default = ["grid_id","billyear","billmonth"]
    in_table_name_default = "WCSR_grid"
    out_table_name_default = "WCSR_grid"
    entity_name_default = "consumption"
    
