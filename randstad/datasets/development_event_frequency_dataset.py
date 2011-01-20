# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DevelopmentEventFrequencyDataset(UrbansimDataset):
    """Set of development constraints."""

    id_name_default = "development_type_id"
    in_table_name_default = "development_event_frequency"
    out_table_name_default = "development_event_frequency"
    dataset_name = "development_event_frequency"
