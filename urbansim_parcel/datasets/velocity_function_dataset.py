# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class VelocityFunctionDataset(UrbansimDataset):
    id_name_default = "velocity_function_id"
    in_table_name_default = "velocity_functions"
    out_table_name_default = "velocity_functions"
    dataset_name = "velocity_function"
