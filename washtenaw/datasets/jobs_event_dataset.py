# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class JobsEventDataset(UrbansimDataset):
    """Set of events that represent deletion/adding/replacing of jobs from/to specific locations.
    """

    id_name_default = ["grid_id", "scheduled_year"]
    in_table_name_default = "jobs_events"
    out_table_name_default = "jobs_events"
    dataset_name = "jobs_event"
