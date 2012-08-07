# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from numpy import where, arange, ones, sum, logical_and, ones_like

class ProcessPipelineEvents(Model):
    """Process any pre-scheduled development events.
       Currently, these can only be from exogenous development events.
    """
    model_name = "ProcessPipelineEvents"
    
    def run (self,scheduled_development_events, buildings, residential_units=None,
             year=None, event_filter=None, scenario_name=None,
             resources=None):

        scheduled_events = scheduled_development_events  #renamed so it is shorter
        known_attributes = scheduled_events.get_known_attribute_names()

        is_matched_scenario = ones(scheduled_events.size(), dtype='bool')
        if scenario_name is not None:
            scenario_name = resources.get('scenario_name', None)
        if 'scenario_name' in known_attributes and scenario_name is not None:
            is_matched_scenario = scheduled_events['scenario_name'] == scenario_name

        if year is None:
            year = SimulationState().get_current_time()
        is_matched_year = scheduled_events['scheduled_year'] == year

        passes_filter = ones(scheduled_events.size(), dtype='bool')
        if event_filter is not None:
            passes_filter = scheduled_events.compute_variables(event_filter)

        indicator = is_matched_scenario & is_matched_scenario & passes_filter 
        
        if indicator.sum() == 0:
            logger.log_status('No scheduled developments.')
            return 

        first_building_id = buildings.get_id_attribute().max() + 1
        first_unit_id = residential_units.get_id_attribute().max() + 1
        new_buildings = {}
        new_units = {}

        new_buildings["building_id"] = first_building_id + arange(indicator.sum())
        new_units["building_id"] = first_building_id + arange(indicator.sum())
        new_units[residential_units.get_id_name()[0]] = first_unit_id + arange(indicator.sum())

        new_buildings['year_built'] = ones(indicator.sum(), dtype="i4") * year
        new_buildings["scheduled_event_id"] = scheduled_events.get_id_attribute()[indicator]
        for attribute in known_attributes:
            new_buildings[attribute] = scheduled_events[attribute][indicator]
            new_units[attribute] = scheduled_events[attribute][indicator]
            #populate residential_units
            
        if 'scheduled_event_id' not in buildings.get_known_attribute_names():
            buildings.add_primary_attribute(-1 * ones_like(buildings.get_id_attribute()),
                                            scheduled_events.get_id_name()[0])

        buildings.add_elements(new_buildings, require_all_attributes=False)
        ##TODO: fix problem with base year - the residential_unit_id is not unique
        residential_units.add_elements(new_units, require_all_attributes=False, change_ids_if_not_unique=True) 

        return

