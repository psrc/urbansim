# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DevelopmentEventTemplateDataset(UrbansimDataset):
    """Set of development constraints."""

    id_name_default = "development_type_id"
    in_table_name_default = "development_event_template"
    out_table_name_default = "development_event_template"
    dataset_name = "development_event_template"
