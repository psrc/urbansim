#
# Opus software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

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