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

from opus_core.class_factory import ClassFactory 

class StorageFactory(object):
    """ Class for creating a Storage object. 
    """        
    def get_storage(self, type, subdir='store', package='opus_core', **kwargs):
        """'type' determines the name of Storage subclass (mysql_storage, flt_storage, ...). There has to be a module 
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