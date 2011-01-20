# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class HouseholdCharacteristicDataset(UrbansimDataset):
    """Set of household characteristics."""

    id_name_default = []
    in_table_name_default = "household_characteristics_for_ht"
    out_table_name_default = "household_characteristics_for_ht"
    dataset_name = "household_characteristic"

        
