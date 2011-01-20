# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, ones, zeros, array, int32, int16

from opus_core.model import Model
from opus_core.misc import DebugPrinter, unique
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory

from urbansim.datasets.development_event_dataset import DevelopmentEventDataset


class DevelopmentEventTransitionModel(Model):
    """From given types of development projects, e.g. 'residential' or 'commercial', create
    development events, one for a gridcell. Only placed projects are considered.
    It returns an object of class DevelopmentEventDataset.
    """
    def __init__(self, resources=None, debuglevel=0):
        self.debug = DebugPrinter(debuglevel)
        self.resources = resources
        self.model_name = "Development Event Transition Model"
        
    def run(self, developments, year=0, landuse_types=None, units=None, resources=None):
#        landuse_types = ['residential', 'commercial', 'industrial', 'governmental']
#        units=['residential_units', 'commercial_sqft','industrial_sqft','governmental_sqft']
        
        if not isinstance(resources, Resources):
            resources = Resources()

        grid_ids_for_project = array([], dtype=int32)
        if developments <> None:
            grid_ids_for_project = developments.get_attribute("grid_id")
        grid_ids_for_project = unique(grid_ids_for_project)
        grid_ids_for_project = grid_ids_for_project[where(grid_ids_for_project>0)]
        
        if len(grid_ids_for_project)==0: return
        sizes = grid_ids_for_project.size
        result_data = {"grid_id": grid_ids_for_project, 
                       "scheduled_year":(year*ones((sizes,), dtype=int16)),
                       "development_type_id": zeros((sizes,),dtype=int16),
                   }
        
        for unit in units:
            result_data[unit] = zeros((sizes,), dtype=int32)
        for project_type in landuse_types:
            result_data["%s_improvement_value" % project_type] = zeros((sizes,), dtype=int32)
            
        grid_idx=0
        for grid_id in grid_ids_for_project:
            w = where(developments.get_attribute('grid_id') == grid_id)[0]
            if w.size>0:
                result_data["development_type_id"][grid_idx] = \
                    developments.get_attribute_by_index("development_type_id", w[0])
                for unit_variable in units:
                    result_data[unit_variable][grid_idx] = \
                        developments.get_attribute_by_index(unit_variable , w).sum()
                    result_data["%s_improvement_value" % unit_variable.split('_')[0]][grid_idx] = \
                        developments.get_attribute_by_index("improvement_value", w).sum()
            grid_idx += 1
            
        storage = StorageFactory().get_storage('dict_storage')

        eventset_table_name = 'eventset'        
        storage.write_table(
                table_name=eventset_table_name,
                table_data=result_data,
            )
        
        eventset = DevelopmentEventDataset(
            in_storage = storage,
            in_table_name = eventset_table_name, 
            id_name=['grid_id', 'scheduled_year'],
            )
            
        self.debug.print_debug('Number of events: ' + str(grid_ids_for_project.size), 3)
        
        return eventset

    def prepare_for_run(self, model_configuration):
        all_types = []
        all_units = []
        for atype in model_configuration['landuse_development_types']:
            all_types.append(atype)
            all_units.append(model_configuration['landuse_development_types'][atype]['units'])
        return  (all_types, all_units)