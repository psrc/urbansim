# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger

class DataExplorer(object):
    def __init__(self, cache_directory, storage_type='flt_storage', package_order=['opus_core']):
        self.cache_directory=cache_directory
        self.storage = StorageFactory().get_storage(storage_type, 
                        storage_location = self.cache_directory)
        self.set_dataset_pool(package_order)
        
    def get_dataset(self, dataset_name, **kwargs):
        """Return a Dataset object of the given name."""
        return self.get_dataset_pool().get_dataset(dataset_name, kwargs)
    
    def get_dataset_pool(self):
        return self.dataset_pool
    
    def set_dataset_pool(self, package_order=['opus_core']):
        self.dataset_pool = DatasetPool(package_order=package_order, storage=self.storage)
    
    def compute_expression(self, attribute_name):
        """Compute any expression and return its values."""
        var_name = VariableName(attribute_name)
        dataset_name = var_name.get_dataset_name()
        ds = self.get_dataset(dataset_name)
        return ds.compute_variables([var_name], dataset_pool=self.get_dataset_pool())

    def get_table_names(self):
        return self.storage.get_table_names()
        
    def run(self):
        logger.log_status('Exploring data in %s' % self.cache_directory)
        logger.log_status('Available tables:')
        logger.log_status(self.get_table_names())
        logger.log_status('\nUse ex.get_dataset(dataset_name) to access data. Optionally, pass an argument id_name for non-standard name of unique identifier.')
        