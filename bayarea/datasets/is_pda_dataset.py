# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class IsPdaDataset(UrbansimDataset):
    
    id_name_default = "is_pda_id"
    in_table_name_default = "is_pdas"
    out_table_name_default = "is_pdas"
    dataset_name = "is_pda"

    def __init__(self, id_values=1, **kwargs):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='is_pdas',
                            table_data= {
                                         'is_pda_id'        :array([0,1]),
                                         'is_pda'    :array([True,False]),
                                         }
                            )

        resources = Resources({
            'in_storage':storage,
            'in_table_name':'is_pdas'
            })

        UrbansimDataset.__init__(self, resources=resources, **kwargs)