#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from opus_core.model import Model
from opus_core.logger import logger
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from numarray import where, arange, ones

class ProcessPipelineEvents(Model):
    """Process any pre-scheduled development events.
       Currently, these can only be from exogenous development events.
    """
    model_name = "ProcessPipelineEvents"
    
    def run (self, building_dataset, year, storage, in_table="development_events_exogenous",
             out_table="development_events_exogenous"):

        if not storage.has_table(in_table):
            logger.log_status('No exogenous developments.')
            return
        
        scheduled_development_events = DevelopmentEventDataset(in_storage=storage, 
                                                     in_table_name=in_table, 
                                                     out_table_name=out_table,
                                                     id_name='event_id')
        scheduled_index = where(scheduled_development_events.get_attribute("scheduled_year")==year)[0]
        scheduled_development_events.subset_by_index(scheduled_index,flush_attributes_if_not_loaded=False)
        
        max_building_id = building_dataset.get_id_attribute().max()
        new_buildings = {}        
        new_buildings["building_id"] = max_building_id + arange(1, scheduled_index.size()+1)
        attained_attributes = ['parcel_id', 'residential_units', 'building_sqft', 'building_use_id', 'blklot']
        for attribute in attained_attributes:
            new_buildings[attribute] = scheduled_development_events.get_attribute(attribute)
        
        new_buildings['year_built'] = ones(scheduled_index.size()) * year
        building_dataset.add_elements(new_buildings, require_all_attributes=False)

        return scheduled_development_events