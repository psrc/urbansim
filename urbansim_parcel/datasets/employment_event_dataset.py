# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset
    
class EmploymentEventDataset(UrbansimDataset):
    """Set of employment events.
    """

    id_name_default = []
    in_table_name_default = "employment_events"
    out_table_name_default = "employment_events"
    dataset_name = "employment_event"
