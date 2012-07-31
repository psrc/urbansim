# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel
from opus_core.session_configuration import SessionConfiguration

class HouseholdLocationChoiceModelByZones(HouseholdLocationChoiceModel):
        
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):

        dataset_pool = SessionConfiguration().get_dataset_pool()
        zone_set = dataset_pool.get_dataset('zone')
        building_set = dataset_pool.get_dataset('building')
        parcel_set = dataset_pool.get_dataset('parcel')
        building_set.add_attribute(name='zone', data=building_set.compute_variables('building.disaggregate(parcel.zone_id)'))

        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        zone_ids = zone_set.get_id_attribute()
        agents_zones = agent_set.get_attribute(zone_set.get_id_name()[0])
        agents_building_types = agent_set.get_attribute('building_type_id')
        for zone_id in zone_ids:
            new_index = where(logical_and(cond_array, (agents_zones == zone_id)*(agents_building_types == 20)))[0]
            #new_index = where(logical_and(new_index1, agents_building_types == 20))[0]
            #logger.log_status("number of agents %s" % new_index.sum())
            self.filter = "(building.building_type_id==20)*(building.zone == %s)" % zone_id
            logger.log_status("HLCM for zonee %s" % zone_id)
            HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            #self.choice_set.flush_dataset() # this (after a while) slows down the simulation considerably
            
        # set the right parcels
        #parcels = agent_set.compute_variables(["household.disaggregate(building.parcel_id)"],
        #                                      dataset_pool = self.dataset_pool)
        #agent_set.modify_attribute(name="parcel_id", data = parcels)
