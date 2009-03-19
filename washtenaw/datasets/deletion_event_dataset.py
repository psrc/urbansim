# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DeletionEventDataset(UrbansimDataset):
    """Set of events that represent deletion of jobs and/or households from specific locations.
    """

    id_name_default = ["grid_id", "scheduled_year"]
    in_table_name_default = "deletion_events"
    out_table_name_default = "deletion_events"
    dataset_name = "deletion_event"
    