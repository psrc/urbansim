# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DevelopmentEventTemplateDataset(UrbansimDataset):
    """Set of development constraints."""

    id_name_default = "development_type_id"
    in_table_name_default = "development_event_template"
    out_table_name_default = "development_event_template"
    dataset_name = "development_event_template"
