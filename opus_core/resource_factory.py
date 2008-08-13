#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory

class ResourceFactory(object):
    """ Class for creating a Resource object. 
    """        
    def get_resources_for_dataset(self, 
              dataset_name, 
              in_storage,
              out_storage,
              resources={},
              in_table_name_pair=(None,None),
              out_table_name_pair=(None,None),
              attributes_pair=(None,None), 
              id_name_pair=(None,None), 
              nchunks_pair=(None,None), 
              debug_pair=(None,None)
              ):
                            
        """Create an object of class Resources to be used in a Dataset object. 
        The created resources are merged with the resources given as an argument 'resources'. 
        The first element
        of each tuple of the remaining arguments contains the desired value, the second element contains 
        the default value which is used if the first element is None. 
        Entries in resources of the same name as the argument values are overwritten if the one of the 
        tuple values is not equal None.
        """
            
        # merge resources with arguments
        local_resources = Resources(resources)
        local_resources.merge_if_not_None({
                "in_storage":in_storage,
                "out_storage":out_storage,
                "nchunks":nchunks_pair[0], "attributes":attributes_pair[0],
                "in_table_name": in_table_name_pair[0], "out_table_name": out_table_name_pair[0],
                "id_name":id_name_pair[0], "debug":debug_pair[0],
                "dataset_name":dataset_name})
            
        # merge resources with default values    
        local_resources.merge_with_defaults({
                "nchunks":nchunks_pair[1], "attributes":attributes_pair[1],
                "in_table_name":in_table_name_pair[1], "out_table_name":out_table_name_pair[1],
                "id_name":id_name_pair[1], "debug":debug_pair[1],
                "dataset_name":dataset_name})
            
        return local_resources