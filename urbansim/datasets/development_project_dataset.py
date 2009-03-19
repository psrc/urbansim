# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_type import AttributeType
from opus_core.misc import DebugPrinter
from opus_core.storage_factory import StorageFactory
from opus_core.resource_factory import ResourceFactory
from opus_core.resources import Resources
from numpy import arange, array, where, transpose

class DevelopmentProjectDataset(Dataset):
    """Set of development projects."""

    id_name_default = "project_id"
    # name of the variable that defines categories (change this value in resources)
    category_variable_name_default = "urbansim.development_project.size_category"
    
    def __init__(self, categories=array([1,]), resources=None, what=None, attribute_name=None, 
                  data=None, names=None, in_storage=None, out_storage=None,
                  in_table_name=None, 
                  attributes=None, 
                  out_table_name=None, id_name=None,
                  nchunks=None, debuglevel=0):
        """
        'what' must be a string, such as 'residential' or 'commercial'.
        """
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating DevelopmentProjectDataset object for %s projects." % what,2)
        
        self.categories = categories
        self.what = what
        self.attribute_name = attribute_name
        attributes_default = AttributeType.PRIMARY
        dataset_name = "development_project"
        nchunks_default = 1

        if data <> None:
            in_storage = StorageFactory().get_storage('dict_storage')
            
            in_storage.write_table(table_name='development_projects', table_data=data)
            in_table_name='development_projects'
        
        resources = ResourceFactory().get_resources_for_dataset(
                dataset_name,
                resources = resources, 
                in_storage = in_storage,
                out_storage = out_storage,
                in_table_name_pair = (in_table_name,None), 
                out_table_name_pair = (out_table_name, None), 
                attributes_pair = (attributes,attributes_default), 
                id_name_pair = (id_name,self.id_name_default), 
                nchunks_pair = (nchunks,nchunks_default), 
                debug_pair = (debug,None)
                )
        
        self.category_variable_name = resources.get("category_variable_name", 
                                                    self.category_variable_name_default)                  
        Dataset.__init__(self,resources = resources)
        
    def get_attribute_name(self):
        return self.attribute_name
        
    def add_submodel_categories(self):
        if self.category_variable_name is not None:
            self.compute_variables([self.category_variable_name])

class DevelopmentProjectCreator(object):
    id_name_default = 'project_id'
    def create_projects_from_history(self, history_table, what, attribute_name, categories):
        """
        Returns a development project created from the information this
        development_event_history table.
        'what' is a string like 'residential' or 'commercial'.
        'attribute_name' is a string like 'residential_units' or 'commercial_sqft'
        """
        history_values = history_table.get_attribute(attribute_name)
        history_values_without_zeros_idx = where(history_values>0)[0]       
        attributes = history_table.get_primary_attribute_names()
        values = arange(history_values_without_zeros_idx.size)
        
        storage = StorageFactory().get_storage('dict_storage')

        project_table_name = 'project'        
        storage.write_table(
                table_name=project_table_name,
                table_data={
                    self.id_name_default:array(range(len(values))),
                    project_table_name:transpose(values),
                    }
            )

        if categories is None:
            resources = Resources({"category_variable_name": None})
        else:
            resources = None
            
        project = DevelopmentProjectDataset(
            resources = resources,
            in_storage = storage, 
            in_table_name = project_table_name,
            categories = categories,
            names = [self.id_name_default], 
            what = what,
            attribute_name = attribute_name,
            )

        for attr in attributes:
            project.add_primary_attribute(history_table.get_attribute_by_index(attr, history_values_without_zeros_idx), attr)
                                  
        project.add_submodel_categories()
        
        return project
    
def create_residential_projects_from_history(history_table):
    creator = DevelopmentProjectCreator()
    return creator.create_projects_from_history(history_table, 'residential', 'residential_units',
                                                categories=array([1,2,3,5,10,20]))
    
def create_commercial_projects_from_history(history_table):
    creator = DevelopmentProjectCreator()
    return creator.create_projects_from_history(history_table, 'commercial', 'commercial_sqft',
                                                categories=1000*array([1, 2, 5, 10]))
    
def create_industrial_projects_from_history(history_table):
    creator = DevelopmentProjectCreator()
    return creator.create_projects_from_history(history_table, 'industrial', 'industrial_sqft',
                                                categories=1000*array([1,2,5,10]))
    
