# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class HouseholdsEventDataset(UrbansimDataset):
    """Set of events that represent deletion/adding/replacing households from/to specific locations.
    """

    id_name_default = ["parcel_id", "scheduled_year"]
    in_table_name_default = "households_events"
    out_table_name_default = "households_events"
    dataset_name = "households_event"
    
    