# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.misc import DebugPrinter, unique
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from opus_core.model import Model
from numpy import where, ones, zeros, array, int32, concatenate #@UnresolvedImport
from opus_core.storage_factory import StorageFactory


class DevelopmentEventTransitionModel(Model):
    """From given types of development projects, e.g. 'residential' or 'commercial', create
    development events, one for a location. Only placed projects are considered.
    It returns an object of class DevelopmentEventDataset.
    """
    model_name = "Development Event Transition Model"
        
    def run(self, projects, types, units, year=0, location_id_name="grid_id", debuglevel=0):
        debug = DebugPrinter(debuglevel)
        grid_ids_for_any_project = array([], dtype=int32)
        grid_ids_by_project_type = {}
        for project_type in types:
            grid_ids_by_project_type[project_type] = array([], dtype=int32)
            if projects[project_type] != None:
                grid_ids_by_project_type[project_type] = projects[project_type].get_attribute(location_id_name)
            grid_ids_for_any_project = unique(concatenate((grid_ids_for_any_project, 
                                                                  grid_ids_by_project_type[project_type])))
        grid_ids_for_any_project = grid_ids_for_any_project[where(grid_ids_for_any_project>0)]
        if not len(grid_ids_for_any_project): return
        
        result_data = {location_id_name: grid_ids_for_any_project, 
                       "scheduled_year":(year*ones((grid_ids_for_any_project.size,))).astype(int32)}
        for unit in units:
            result_data[unit] = zeros((grid_ids_for_any_project.size,), dtype=int32)
        for project_type in types:
            result_data["%s_improvement_value" % project_type] = zeros((grid_ids_for_any_project.size,), dtype=int32)
            
        grid_idx=0
        for grid_id in grid_ids_for_any_project:
            for i in range(0,len(types)):
                project_type = types[i]
                my_projects = projects[project_type]
                w = where(my_projects.get_attribute(location_id_name) == grid_id)[0]
                if w.size>0:
                    unit_variable = units[i]
                    result_data[unit_variable][grid_idx] = \
                        my_projects.get_attribute_by_index( 
                            my_projects.get_attribute_name(), w).sum()
                    result_data["%s_improvement_value" % project_type][grid_idx] = \
                        my_projects.get_attribute_by_index( 
                            "improvement_value", w).sum()
            grid_idx += 1  
        
        storage = StorageFactory().get_storage('dict_storage')

        eventset_table_name = 'development_events_generated'        
        storage.write_table(table_name=eventset_table_name, table_data=result_data)

        eventset = DevelopmentEventDataset(
            in_storage = storage, 
            in_table_name = eventset_table_name, 
            id_name = [location_id_name, "scheduled_year"],
            ) 
                                      
        debug.print_debug("Number of events: " + str(grid_ids_for_any_project.size), 3)
        return eventset

    def prepare_for_run(self, dev_projects, development_models = None, 
                        models_configuration = None, model_configuration = None):
        """
        dev_projects: output from development projects
        development_models: list of development models to get project data from
        model[s]_configuration: configuration objects used to get data for
                                development project models. The singular
                                model_configuration is used when 
                                development_models is None, otherwise the plural 
                                models_configuration is used.
        """
        # argument check
        if development_models is not None and models_configuration is None:
            raise Exception('Configurations that pass a list of development'
                                ' models (argument: "development_models") must '
                                'also pass a reference to the entire models '
                                'configuration (argument: "models_'
                                'configuration") note: plural model[s].')

        dev_model_configs = {}
        if development_models is None: # assume this means that we use old conf
            # try to get a reference to the external information for development
            # project types
            try:
                dev_model_configs = model_configuration['development_project_types']
            except:
                dev_model_configs = models_configuration['development_project_types']
        else:
            # pull in information from the specified development project models
            for dev_proj_model in development_models:
                model_conf = models_configuration[dev_proj_model]
                proj_type = model_conf['controller']['init']['arguments']['project_type'].strip('\'"')
                dev_model_configs[proj_type] = {}
                dev_model_configs[proj_type]['units'] = model_conf['controller']['init']['arguments']['units'].strip('\'"')
                dev_model_configs[proj_type]['residential'] = model_conf['controller']['init']['arguments']['residential']
                dev_model_configs[proj_type]['categories'] = model_conf['controller']['prepare_for_estimate']['arguments']['categories']

        all_project_types = []
        all_project_units = []
                    
        for project_type in dev_model_configs:
            if dev_projects[project_type] is not None:
                all_project_types.append(project_type)
                all_project_units.append(dev_model_configs[project_type]['units'])
        return  (all_project_types, all_project_units)