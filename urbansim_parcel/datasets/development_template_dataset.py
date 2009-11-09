# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DevelopmentTemplateDataset(UrbansimDataset):
    """development template.
    """
    in_table_name_default = "development_templates"
    out_table_name_default = "development_templates"
    dataset_name = "development_template"
    id_name_default = "template_id"
