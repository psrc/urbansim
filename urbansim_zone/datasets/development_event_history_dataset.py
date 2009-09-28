# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim_zone.datasets.development_event_dataset import DevelopmentEventDataset

class DevelopmentEventHistoryDataset(DevelopmentEventDataset):
    """Set of development events from the history.
    """
    id_name_default = []
    in_table_name_default = "development_event_history"
    out_table_name_default = "development_event_history"
    dataset_name = "development_event_history"
