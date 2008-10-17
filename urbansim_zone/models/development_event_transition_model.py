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

from opus_core.misc import unique_values
from urbansim_zone.datasets.development_event_dataset import DevelopmentEventDataset
from opus_core.model import Model
from numpy import where, ones, zeros, array, int32, concatenate
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger

class DevelopmentEventTransitionModel(Model):
    """From given types of development projects, e.g. 'residential' or 'commercial', create
    development events, one for a location. Only placed projects are considered.
    It returns an object of class DevelopmentEventDataset.
    """
    model_name = "Development Event Transition Model"
        
    def run(self, projects, year=0, location_id_name="zone_id", units_names = {}):
        project_types = projects.keys()
        project_units_names = units_names
        for ptype in project_types:
            if (ptype not in project_units_names) and (projects[ptype] is not None):
                pattrs = projects[ptype].get_primary_attribute_names()
                pattrs.remove(location_id_name)
                pattrs.remove(projects[ptype].get_id_name()[0])
                project_units_names[ptype] = pattrs[0] 
        loc_ids_for_any_project = array([], dtype=int32)
        loc_ids_by_project_type = {}
        for project_type in project_types:
            loc_ids_by_project_type[project_type] = array([], dtype=int32)
            if projects[project_type] is not None:
                loc_ids_by_project_type[project_type] = projects[project_type].get_attribute(location_id_name)
            loc_ids_for_any_project = unique_values(concatenate((loc_ids_for_any_project, 
                                                                  loc_ids_by_project_type[project_type])))
        loc_ids_for_any_project = loc_ids_for_any_project[where(loc_ids_for_any_project>0)]
        if loc_ids_for_any_project.size <= 0: 
            return None
        
        result_data = {location_id_name: loc_ids_for_any_project, 
                       "scheduled_year":(year*ones((loc_ids_for_any_project.size,))).astype(int32)}

        for project_type in project_units_names.keys():
            result_data[project_units_names[project_type]] = zeros((loc_ids_for_any_project.size,), dtype=int32)
            
        for loc_idx in range(loc_ids_for_any_project.size):
            for project_type in project_units_names.keys():
                my_projects = projects[project_type]
                w = where(my_projects.get_attribute(location_id_name) == loc_ids_for_any_project[loc_idx])[0]
                if w.size>0:
                    unit_variable = project_units_names[project_type]
                    result_data[unit_variable][loc_idx] = \
                        my_projects.get_attribute_by_index( 
                            my_projects.get_attribute_name(), w).sum()
        
        storage = StorageFactory().get_storage('dict_storage')

        eventset_table_name = 'development_events_generated'        
        storage.write_table(table_name=eventset_table_name, table_data=result_data)

        eventset = DevelopmentEventDataset(
            in_storage = storage, 
            in_table_name = eventset_table_name, 
            id_name = [location_id_name, "scheduled_year"],
            ) 
                                      
        logger.log_status("Number of events: " + str(loc_ids_for_any_project.size))
        return eventset
