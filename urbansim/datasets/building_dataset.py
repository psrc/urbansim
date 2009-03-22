# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import re
from numpy import array, where, ones, zeros, arange
from opus_core.resources import Resources
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingDataset(UrbansimDataset):
    
    id_name_default = "building_id"
    in_table_name_default = "buildings"
    out_table_name_default = "buildings"
    dataset_name = "building"
    default_categories = {}
    default_categories["residential"] = array([1,2,3,5,10,20])
    default_categories["commercial"] = 1000*array([1, 2, 5, 10])
    default_categories["industrial"] = 1000*array([1,2,5,10])
    default_categories["governmental"] = array([], dtype='int32')
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
    def get_categories(self, type):
        """Returns an entry "building_categories" from self.resources for the given type.
        The entry can be put into the resources e.g. through the constructor.
        """
        categories = self.resources.get("building_categories", self.default_categories)
        return categories.get(type, array([], dtype='int32'))
        
from opus_core.storage_factory import StorageFactory
        
class BuildingCreator(object):

    def create_buildings_from_history(self, history_table, type, type_code, units, building_categories):
        """
        Returns a BuildingDataset created from the information this
        development_event_history table.
        'type' is the type of the buildings ('residential' or 'commercial')
        'type_code' is an interger code for the corresponding building type.
        'units' is a string like 'residential_units' or 'commercial_sqft'.
        """
        history_values = history_table.get_attribute(units)
        history_values_without_zeros_idx = where(history_values>0)[0]
        nbuildings = history_values_without_zeros_idx.size
        ids = arange(nbuildings)
        grid_ids = history_table.get_attribute_by_index("grid_id", history_values_without_zeros_idx)
        
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='buildings',
            table_data={
                BuildingDataset.id_name_default: ids, 
                "grid_id" : grid_ids,
                "building_type_id": type_code*ones(nbuildings), 
                "sqft": zeros(nbuildings),
                "residential_units": zeros(nbuildings),
                "year_built": history_table.get_attribute_by_index("scheduled_year", history_values_without_zeros_idx),
                "improvement_value": history_table.get_attribute_by_index("%s_improvement_value" % type, 
                                                                          history_values_without_zeros_idx)
                }
            )            
        if re.search("sqft", units):
            attr_name = "sqft"
        else:
            attr_name = "residential_units"
        buildings = BuildingDataset(in_storage=storage, in_table_name='buildings',
            resources=Resources({"building_categories": building_categories})
            )
        buildings.modify_attribute(attr_name, history_table.get_attribute_by_index(units, history_values_without_zeros_idx))
        return buildings
    
    def add_events_from_history_to_existing_buildings(self, buildings, history_table, type, type_code, units, 
                                                         building_categories, dataset_pool=None):
        """ Creates buildings of given type from event history and adds them to an existing buildings dataset 'buildings'. It recomputes
        the variables size_category_SSS and building_age.
        """
        buildings_from_history = self.create_buildings_from_history(history_table, type, type_code, units, building_categories)
        buildings.join_by_rows(buildings_from_history, change_ids_if_not_unique=True)
        buildings.compute_variables(["urbansim.%s.size_category_%s" % (buildings.get_dataset_name(), type),
                                     "urbansim.%s.building_age" % buildings.get_dataset_name()],                                           
                           dataset_pool=dataset_pool)
        
    def create_all_buildings_from_history(self, history_table, building_types):
        """Creates buildings of all types from history"""
        type_ids = building_types.get_id_attribute()
        buildings = self.create_buildings_from_history(history_table, building_types.get_attribute("name")[0],
                                              type_ids[0], building_types.get_attribute("units")[0],
                                               BuildingDataset.default_categories[building_types.get_attribute("name")[0]])
        for iid in range(1,type_ids.size):
            buildings_of_this_type = self.create_buildings_from_history(history_table, 
                                                building_types.get_attribute("name")[iid],
                                              type_ids[iid], building_types.get_attribute("units")[iid],
                                               BuildingDataset.default_categories[building_types.get_attribute("name")[iid]])
            buildings.join_by_rows(buildings_of_this_type, change_ids_if_not_unique=True)
        return buildings   

