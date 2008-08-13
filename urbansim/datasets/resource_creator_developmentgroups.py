#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.variables.attribute_type import AttributeType
from opus_core.resource_factory import ResourceFactory
from urbansim.opus_package_info import package

class ResourceCreatorDevelopmentGroups(object):                
    def get_resources_for_dataset(self, 
            resources=None, 
            in_storage=None, 
            out_storage=None, 
            in_table_name=None, 
            out_table_name=None, 
            in_table_name_groups=None, 
            attributes=None, 
            id_name_default=None,
            id_name=None, 
            nchunks=None, 
            debug=None,
            ):
        # Defaults:
        in_table_name_default = "development_type_groups"
        attributes_default = AttributeType.PRIMARY
        out_table_name_default = "development_type_groups"
        dataset_name = "development_group"
        nchunks_default = 1
        
        resources = ResourceFactory().get_resources_for_dataset(
                dataset_name,
                resources=resources, 
                in_storage=in_storage,
                out_storage=out_storage,
                in_table_name_pair=(in_table_name,in_table_name_default), 
                attributes_pair=(attributes,attributes_default), 
                out_table_name_pair=(out_table_name, out_table_name_default), 
                id_name_pair=(id_name,id_name_default),
                nchunks_pair=(nchunks,nchunks_default),                 
                debug_pair=(debug,None)
                )
          
        resources.merge({"replace_nulls_with":"None"})
                
        return resources