# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.attribute_type import AttributeType
from opus_core.resource_factory import ResourceFactory
from urbansim.opus_package_info import package

class ResourceCreatorEmploymentSectorGroups(object):                
    def get_resources_for_dataset(self, 
            resources=None, 
            in_storage=None, 
            out_storage=None,
            in_table_name=None, 
            in_table_name_groups=None, 
            out_table_name=None, 
            attributes=None, 
            id_name=None, 
            id_name_default=None,
            nchunks=None, 
            debug=None
            ):
        # Defaults:
        in_table_name_default = "employment_adhoc_sector_groups"
        attributes_default = AttributeType.PRIMARY
        out_table_name_default = "employment_adhoc_sector_groups"
        dataset_name = "employment_sector_group"
        nchunks_default = 1
        
        resources = ResourceFactory().get_resources_for_dataset(
            dataset_name,
            resources = resources, 
            in_storage = in_storage,
            out_storage = out_storage,
            in_table_name_pair = (in_table_name,in_table_name_default), 
            attributes_pair = (attributes,attributes_default), 
            out_table_name_pair = (out_table_name, out_table_name_default), 
            id_name_pair = (id_name,id_name_default), 
            nchunks_pair = (nchunks,nchunks_default),                
            debug_pair = (debug,None)
            )
          
        resources.merge({"replace_nulls_with":"None"})
                
        return resources