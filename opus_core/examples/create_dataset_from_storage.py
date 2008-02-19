#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import os
from opus_core.storage_factory import StorageFactory
from opus_core.opus_package import OpusPackage
from opus_core.datasets.dataset import Dataset

def create_dataset_from_tab_storage():
    storage = StorageFactory().get_storage('tab_storage', # type of storage
                                           storage_location = os.path.join(OpusPackage().get_opus_core_path(), "data/tab") # directory
                                           )
    test_dataset = Dataset(in_storage = storage, 
                           in_table_name='tests', # file name without its ending
                           id_name='id' # which attribute is the unique identifier
                           )
    return test_dataset

def create_dataset_from_tab_storage_shortcut():
    from opus_core.misc import get_dataset_from_tab_storage
    return get_dataset_from_tab_storage('tests', 
                                        directory=os.path.join(OpusPackage().get_opus_core_path(), "data/tab"),
                                        dataset_args={'in_table_name':'tests', 'id_name':'id'})
    
if __name__ == "__main__":
    ds = create_dataset_from_tab_storage()
    ds.summary()
    ds = create_dataset_from_tab_storage_shortcut()
    ds.summary()