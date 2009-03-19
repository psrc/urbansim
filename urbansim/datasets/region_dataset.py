# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import array
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory

class RegionDataset(UrbansimDataset):

    id_name_default = 'region_id'
    in_table_name_default = 'regions'
    out_table_name_default = 'regions'
    dataset_name = 'region'

    def __init__(self, id_values=1, **kwargs):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='regions',
            table_data={
                self.id_name_default:array([id_values])
                }
            )

        resources = Resources({
            'in_storage':storage,
            'in_table_name':'regions'
            })

        UrbansimDataset.__init__(self, resources=resources, **kwargs)

#        if id_values <> None:
#            self._add_id_attribute(data=arrayid_values, name=self.get_id_name()[0])
#        self._create_id_mapping_array()
#
#    def _update_id_mapping(self):
#        UrbansimDataset._update_id_mapping(self)
#        self._create_id_mapping_array()
#
#    def _create_id_mapping_array(self):
#        ids = self.get_id_attribute()
#        self.__id_mapping_array = -1*ones(ids.max())
#        self.__id_mapping_array[self.get_id_attribute()-1] = self.get_id_index(ids)
