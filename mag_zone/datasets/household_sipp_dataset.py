# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import sort, where, array

class HouseholdSippDataset(UrbansimDataset):
    """Set of SIPP households."""

    id_name_default = "household_id"
    in_table_name_default = "households_sipp"
    out_table_name_default = "households_sipp"
    dataset_name = "household_sipp"
    
    def __init__(self, *args, **kwargs):
        UrbansimDataset.__init__(self, *args, **kwargs)               