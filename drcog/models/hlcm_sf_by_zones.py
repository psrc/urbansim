# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel
from opus_core.session_configuration import SessionConfiguration

class HlcmSfByZones(HouseholdLocationChoiceModel):
        
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        dataset_pool = SessionConfiguration().get_dataset_pool()
        zones = dataset_pool.get_dataset('zone')
        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        zone_ids = zones.get_id_attribute()
        agents_zones = agent_set.get_attribute(zones.get_id_name()[0])
        agents_building_types = agent_set.get_attribute("building_type_id")
        for zone_id in zone_ids:
            new_index = where(logical_and(cond_array, (agents_zones == zone_id)*(agents_building_types == 20)))[0]
            self.filter = "(building.building_type_id==20)*(building.zone_id == %s)" % zone_id
            logger.log_status("HLCM for zone %s" % zone_id)
            HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            #self.choice_set.flush_dataset() # this (after a while) slows down the simulation considerably
            
        # set the right parcels
        #parcels = agent_set.compute_variables(["household.disaggregate(building.parcel_id)"],
        #                                      dataset_pool = self.dataset_pool)
        #agent_set.modify_attribute(name="parcel_id", data = parcels)