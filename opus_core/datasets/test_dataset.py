# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array
from opus_core.datasets.dataset import Dataset

class TestDataset(Dataset):
    """Dataset for unit tests.
    """
    
    def __init__(self, *args, **kwargs):
        Dataset.__init__(
            self, 
            dataset_name="test",
            id_name="id",
            in_table_name=kwargs.get('in_table_name','tests'),
            in_storage=kwargs['in_storage']
        )
