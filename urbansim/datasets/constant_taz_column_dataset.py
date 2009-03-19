# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ConstantTazColumnDataset(UrbansimDataset):
    id_name_default = ["taz", "year"]
    in_table_name_default = "constant_taz_columns"
    out_table_name_default = "constant_taz_columns"
    dataset_name = "constant_taz_column"
    
