# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ConstantTazColumnDataset(UrbansimDataset):
    id_name_default = ["taz", "year"]
    in_table_name_default = "constant_taz_columns"
    out_table_name_default = "constant_taz_columns"
    dataset_name = "constant_taz_column"
    
