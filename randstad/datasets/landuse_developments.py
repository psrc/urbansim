# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import arange, where, transpose

from opus_core.misc import DebugPrinter
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from opus_core.resource_factory import ResourceFactory
from opus_core.variables.attribute_type import AttributeType

class LandUseDevelopmentDataset(Dataset):
    """Set of landuse developments."""

    id_name_default = "landuse_development_id"
    def __init__(self, 
            resources=None, 
            data=None, 
            names=None, 
            in_storage=None, 
            out_storage=None,
            in_table_name=None, 
            out_table_name=None,
            attributes=None, 
            id_name=None,
            nchunks=None, 
            debuglevel=0
            ):
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating LandUseDevelopmentDataset object.", 2 )
        
        dataset_name = "landuse_development"
        nchunks_default = 1
        
        if data <> None:
            in_storage = StorageFactory().get_storage('dict_storage')
            
            in_storage.write_table(table_name='landuse_developments', table_data=data)
            in_table_name='landuse_developments'
        
        resources = ResourceFactory().get_resources_for_dataset(
                dataset_name, 
                in_storage=in_storage, 
                out_storage=out_storage,
                resources=resources, 
                in_table_name_pair=(in_table_name,None), 
                out_table_name_pair=(out_table_name, None), 
                id_name_pair=(id_name,self.id_name_default), 
                nchunks_pair=(nchunks,nchunks_default), 
                debug_pair=(debug,None)
                )
            
        Dataset.__init__(self, resources = resources)
        
    
def create_landuse_developments_from_history(history_table, attribute_name='development_type_id'):
    """
    """
    id_name_default = 'landuse_development_id'
    history_values_starting = history_table.get_attribute('starting_' + attribute_name)
    history_values_ending = history_table.get_attribute('ending_' + attribute_name)
    development_index = where(history_values_starting<>history_values_ending)[0]
    #attributes = history_table.get_primary_attribute_names()
    attributes = ['scheduled_year', 'grid_id']
    values = arange(development_index.size)
    
    storage = StorageFactory().get_storage('dict_storage')
    
    development_table_name = 'development'
    storage.write_table(
            table_name=development_table_name,
            table_data=transpose(values),
        )
    
    development = LandUseDevelopmentDataset(
        in_storage = storage, 
        in_table_name = development_table_name,
        names = [id_name_default]
        )
    
    for attr in attributes:
        development.add_attribute(history_table.get_attribute_by_index(attr, development_index),
                                  attr, metadata=AttributeType.PRIMARY)
    #load ending_development_type_id as development_type_id
    development.add_attribute(history_table.get_attribute_by_index('ending_development_type_id', development_index), 
                              attribute_name, metadata=AttributeType.PRIMARY)
    #project.add_submodel_categories()
    return development