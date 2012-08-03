# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class IsPdaXCountyDataset(UrbansimDataset):
    id_name_default = "is_pda_x_county_id"
    in_table_name_default = "is_pda_x_county"
    out_table_name_default = "is_pda_x_county"
    dataset_name = "is_pda_x_county"
    
    id_values = array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],dtype='i4')
    
    def __init__(self, id_values=id_values, **kwargs):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name=self.in_table_name_default,
                            table_data= {
                                         self.id_name_default: id_values,
                                         }
                            )

        kwargs.update({'in_storage': storage})
        UrbansimDataset.__init__(self, **kwargs)

