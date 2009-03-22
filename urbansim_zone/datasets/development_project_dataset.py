# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_type import AttributeType
from opus_core.misc import DebugPrinter
from opus_core.storage_factory import StorageFactory
from opus_core.resource_factory import ResourceFactory
from numpy import arange, array, where, transpose
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset as USDevelopmentProjectDataset
class DevelopmentProjectDataset(USDevelopmentProjectDataset):
    """Set of development projects."""

    category_variable_name_default = None
    
class DevelopmentProjectCreator(object):
    id_name_default = 'project_id'
    def create_projects_from_history(self, history_table, what, attribute_name, categories=None):
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
                    self.id_name_default:arange(values.size)+1,
                    project_table_name:transpose(values),
                    }
            )

        project = DevelopmentProjectDataset(
            in_storage = storage, 
            in_table_name = project_table_name,
            names = [self.id_name_default], 
            what = what,
            attribute_name = attribute_name,
            categories=categories
            )

        for attr in attributes:
            project.add_attribute(history_table.get_attribute_by_index(attr, history_values_without_zeros_idx),
                                  attr, metadata=AttributeType.PRIMARY)
                                  
        project.add_submodel_categories()
        
        return project
    
