# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ActivityDataset(UrbansimDataset):
    id_name_default = "activity_id"
    in_table_name_default = "activities"
    out_table_name_default = "activities"
    dataset_name = "activity"
