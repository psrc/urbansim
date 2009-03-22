# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.class_factory import ClassFactory 

class StorageFactory(object):
    """ Class for creating a Storage object. 
    """        
    def get_storage(self, type, subdir='store', package='opus_core', **kwargs):
        """'type' determines the name of Storage subclass (sql_storage, flt_storage, ...). There has to be a module 
        of that name that contains a class of the same name. 'resources' is passed to the constructor of the 
        Storage class. The argument 'subdir' gives the name of a subdirectory in which the storage class resides.
        """        
        if subdir:
            module_name  = package + "." + subdir + "." + type 
        else:
            module_name  = package + "." + type 
        return ClassFactory().get_class(module_name, arguments=kwargs)

    def build_storage_for_dataset(self, type, subdir='store', package='opus_core', **kwargs):
        """Like 'get_storage', additionally it creates 'resources' within the method, with an entry 
        'storage_location'.
        If 'type' is not equal None, return a storage object, otherwise None."""
        if type is None:
            return None
            
        return self.get_storage(type=type, subdir=subdir, package=package, **kwargs)