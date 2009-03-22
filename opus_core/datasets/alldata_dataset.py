# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory


class AlldataDataset(Dataset):
    """Special dataset for summaries over all members of other datasets. It has only one member.
       (to be used with the built-in function aggregate_all)
    """
    
    def __init__(self, *args, **kwargs):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='alldata',
            table_data={
                'id':array([1]),
                }
            )
        
        Dataset.__init__(self, in_storage=storage, in_table_name='alldata', id_name="id", dataset_name="alldata")
    
    def flush_dataset(self):
        # no flushing is allowed for this dataset
        pass