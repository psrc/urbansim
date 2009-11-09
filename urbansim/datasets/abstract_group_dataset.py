# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_type import AttributeType
from opus_core.resource_factory import ResourceFactory
from numpy import where, array, ndarray, resize

class AbstractGroupDataset(Dataset):
    """Abstract dataset class for datasets that have groups."""

    id_name_default = None
    group_id_name = None

    def __init__(self,
            resources=None,
            other_in_table_names=None,
            use_groups=True,
            ):

        Dataset.__init__(self,resources = resources)

        if isinstance(other_in_table_names,list):
            for place_name in other_in_table_names: #load other tables
                ds = Dataset(resources = resources)
                ds.load_dataset(in_table_name=place_name)
                self.connect_datasets(ds)

        if use_groups:
            self.groups = self._get_groups()

    def are_in_group(self, ids, group):
        id_indices = self.get_id_index(ids)
        def func(idx):
            try:
                return group in self.groups[idx,:]
            except:
                return False
        return array(map(lambda x: func(x), id_indices))

    def get_types_for_group(self, group):
        ids = self.get_id_attribute()
        is_group = array(map(lambda idx: group in self.groups[idx,:], range(self.size())), dtype="bool8")
        return ids[is_group]

    def _get_groups(self):
        self._ensure_id_attribute_is_loaded()
        data = self.resources["in_storage"].load_table(
            table_name=self.resources["in_table_name_groups"],
            column_names=[self.get_id_name()[0], self.group_id_name],
            )
        return self._create_group_array(data, self.get_id_name()[0], self.group_id_name,
                                   self.id_mapping, self.id_mapping_shift)

    def flush_dataset(self):
        Dataset.flush_dataset(self)
        group_dataset = Dataset(in_storage=self.resources["in_storage"],
                                in_table_name=self.resources["in_table_name_groups"],
                                id_name=[self.get_id_name()[0], self.group_id_name])
        group_dataset.load_dataset()
        group_dataset.flush_dataset()
        
    def _create_group_array(self, dict_data, id_name, group_id_name, id_mapping, shift=0):
        used_ids = []
        if isinstance(id_mapping, ndarray):
            length = id_mapping.size
        else:
            length = len(id_mapping.keys())
        result = resize(array([-9999], dtype='int32'), (length, len(dict_data[group_id_name])))
        for i in range(len(dict_data[id_name])):
            id = dict_data[id_name][i]
            if id not in used_ids:
                idx = where(dict_data[id_name]==id)[0]
                if idx.size > 0:
                    if isinstance(id_mapping, ndarray):
                        result[id_mapping[id-shift],range(0,idx.size)] = dict_data[group_id_name][idx]
                    else:
                        result[id_mapping[id], range(0,idx.size)] = dict_data[group_id_name][idx]
                used_ids.append(id)
    
        return result
    
    def _get_resources_for_dataset(self,
            in_table_name_default,
            in_table_name_groups_default,
            out_table_name_default,
            dataset_name,
            resources=None,
            in_storage=None,
            out_storage=None,
            in_table_name=None,
            in_table_name_groups=None,
            attributes=None,
            out_table_name=None,
            id_name=None,
            id_name_default=None,
            debug=None,
            ):
        # Defaults:
        attributes_default = AttributeType.PRIMARY
        
        resources = ResourceFactory().get_resources_for_dataset(
                dataset_name,
                resources = resources, 
                in_storage = in_storage,
                out_storage = out_storage,
                in_table_name_pair = (in_table_name,in_table_name_default), 
                attributes_pair = (attributes,attributes_default), 
                out_table_name_pair = (out_table_name, out_table_name_default), 
                id_name_pair = (id_name,id_name_default), 
                debug_pair = (debug,None),
                )
                
        resources.merge_if_not_None({"in_table_name_groups":in_table_name_groups})
        resources.merge_with_defaults({"in_table_name_groups":in_table_name_groups_default})
        return resources

