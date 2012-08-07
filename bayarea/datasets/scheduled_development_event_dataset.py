# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ScheduledDevelopmentEventDataset(UrbansimDataset):
    
    id_name_default = ['scheduled_event_id']
    in_table_name_default = "scheduled_development_events"
    out_table_name_default = "scheduled_development_events"
    dataset_name = "scheduled_development_event"


