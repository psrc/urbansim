# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class JobsEventDataset(UrbansimDataset):
    """Set of events that represent deletion/adding/replacing of jobs from/to specific locations.
    """

    id_name_default = ["grid_id", "scheduled_year"]
    in_table_name_default = "jobs_events"
    out_table_name_default = "jobs_events"
    dataset_name = "jobs_event"
