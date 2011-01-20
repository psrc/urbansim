# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DeletionEventDataset(UrbansimDataset):
    """Set of events that represent deletion of jobs and/or households from specific locations.
    """

    id_name_default = ["grid_id", "scheduled_year"]
    in_table_name_default = "deletion_events"
    out_table_name_default = "deletion_events"
    dataset_name = "deletion_event"
    