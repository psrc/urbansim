# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, unique
from opus_core.logger import logger
from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel
from opus_core.session_configuration import SessionConfiguration

class HouseholdLocationChoiceModelByZonetypes(HouseholdLocationChoiceModel):
    model_name = "HouseholdAllocationtoBuildingModel"
    model_short_name = "HATBM"
        
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):

        dataset_pool = SessionConfiguration().get_dataset_pool()
        #county_set = dataset_pool.get_dataset('county')
        building_set = dataset_pool.get_dataset('building')
        #building_set.add_attribute(name='submarket', data=building_set.compute_variables('bayarea.building.submarket_id'))

        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        #county_ids = county_set.get_id_attribute()
        agents_zonetypes = agent_set.get_attribute('zonetype')
        zonetype_ids = unique(building_set.get_attribute('zonetype'))#unique(agents_zonetypes)
        for zonetype_id in zonetype_ids:
            new_index = where(logical_and(cond_array, agents_zonetypes == zonetype_id))[0]
            self.filter = "building.zonetype == %s" % zonetype_id
            logger.log_status("HLCM for zonetype %s" % zonetype_id)
            logger.log_status("HLCM for households %s" % agent_set['household_id'][new_index])
            HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            #self.choice_set.flush_dataset() # this (after a while) slows down the simulation considerably
            
        # set the right parcels
        #parcels = agent_set.compute_variables(["household.disaggregate(building.parcel_id)"],
        #                                      dataset_pool = self.dataset_pool)
        #agent_set.modify_attribute(name="parcel_id", data = parcels)
