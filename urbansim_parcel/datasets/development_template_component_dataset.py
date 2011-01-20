# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class DevelopmentTemplateComponentDataset(UrbansimDataset):
    """stores information on components of development templates
    """
    in_table_name_default = "development_template_components"
    out_table_name_default = "development_template_components"
    dataset_name = "development_template_component"
    id_name_default = "component_id"
