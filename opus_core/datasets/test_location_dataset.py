# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from numpy import array
from opus_core.datasets.dataset import Dataset

class TestLocationDataset(Dataset):
    """Dataset for unit tests.  Test version of a dataset of locations, for example gridcells.
    """
    
    def __init__(self, *args, **kwargs):
        Dataset.__init__(
            self, 
            dataset_name="test_location",
            id_name="id",
            in_table_name=kwargs.get('in_table_name','test_locations'),
            in_storage=kwargs['in_storage']
        )
