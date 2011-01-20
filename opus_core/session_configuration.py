# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.logger import logger
from opus_core.singleton import Singleton
from opus_core.general_resources import GeneralResources
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.opus_package_info import package as corepackage


class SessionConfiguration(Singleton, GeneralResources):
    """Maintains a pool of dataset objects, for sharing among models.
    
    The pool has at most one copy of each dataset.
    Datasets are put in the pool lazily; only when that dataset is requested.
    """
    
    # defaults
    dataset_subdirectory = "datasets" # where dataset modules are stored
    dataset_package = "opus_core" # in what package the dataset modules are implemented
    
    def __init__(self, 
                 data={}, 
                 new_instance=False, # Even though this is not used here, 
                     # opus_core.singleton intercepts this argument in its definition 
                     # of __new__.
                 package_order=['opus_core'],
                 in_storage=None
                 ):
        if self.is_new_instance(): # This is set by opus_core.singleton.__new__
            GeneralResources.__init__(self)
            
            if in_storage is None:
                raise Exception("Missing required parameter 'in_storage'.")
            
            self.exceptions_in_storage = None
            self.exceptions_out_storage = None
            self.exceptions_in_table_names = None
            self.exceptions_out_table_names = None
            
            # Info used to create the dataset pool.
            self.package_order = package_order
            self.in_storage = in_storage
            
            self.dataset_pool = None
        self.put_data(data)
        if in_storage is not None:
            self['in_storage'] = in_storage
        
    # TODO: Delete the set_exception... methods.
    def set_exceptions_in_storage(self, data):
        self.exceptions_in_storage = data
        
    def set_exceptions_out_storage(self, data):
        self.exceptions_out_storage = data
        
    def set_exceptions_in_table_names(self, data):
        self.exceptions_in_table_names = data
        
    def set_exceptions_out_table_names(self, data):
        self.exceptions_out_table_names = data
        
    def get_exception(self, exception, object_name):
        if (exception <> None) and (object_name in exception):
            return exception[object_name]
        return None 
            
    def set_in_storage(self, in_storage):
        if self._in_storage != in_storage:
            self.get_dataset_pool().remove_all_datasets()
            self._in_storage = in_storage
            
    def get_dataset_pool(self):
        """Return the DatasetPool object."""
        if self.dataset_pool is None:
            self.dataset_pool = DatasetPool(
                self.package_order,
                storage=self.in_storage)
            
        return self.dataset_pool
    
    def get_dataset_from_pool(self, dataset_name, dataset_arguments = {}):
        """Return the object of this dataset from this dataset pool.
        """
        return self.get_dataset_pool().get_dataset(dataset_name, dataset_arguments = dataset_arguments)

    def delete_datasets(self):
        self.get_dataset_pool().remove_all_datasets()
        # TODO: remove rest of this method, once not being used.
        from opus_core.datasets.dataset import Dataset
        for item in self.keys():
            if isinstance(self[item], Dataset):
                del self[item]
                
    def put_data(self, data):
        self.merge(data)

    def set_dataset_package(self, dataset_package):
        self.dataset_package = dataset_package
                                                                  