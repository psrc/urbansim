'''
Created on Nov 30, 2012

@author: zoelligc
'''
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class LivingUnitsHistoryDataset(UrbansimDataset):
    """Set of living units associated development events from the history.
    """
    in_table_name_default = "living_units_history"
    out_table_name_default = "living_units_history"
    dataset_name = "living_units_history"
    id_name_default = "living_unit_id"

    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)