# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingSqftPerEmployeeDataset(UrbansimDataset):
    
    id_name_default = ['employment_submarket_id']
    in_table_name_default = "building_sqft_per_employee"
    out_table_name_default = "building_sqft_per_employee"
    dataset_name = "building_sqft_per_employee"

