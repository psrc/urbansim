# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel
from opus_core.session_configuration import SessionConfiguration

class EstablishmentLocationChoiceModelBySubmarkets(HouseholdLocationChoiceModel):
        
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):

        dataset_pool = SessionConfiguration().get_dataset_pool()
        submarket_set = dataset_pool.get_dataset('employment_submarket')
        building_set = dataset_pool.get_dataset('building')
        building_set.add_attribute(name='employment_submarket', data=building_set.compute_variables('honolulu_parcel.building.employment_submarket_id'))

        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        submarket_ids = submarket_set.get_id_attribute()
        agents_submarkets = agent_set.get_attribute(submarket_set.get_id_name()[0])
        for submarket_id in submarket_ids:
            new_index = where(logical_and(cond_array, agents_submarkets == submarket_id))[0]
            self.filter = "building.employment_submarket == %s" % submarket_id
            logger.log_status("BLCM for employment_submarket %s" % submarket_id)
            HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            #self.choice_set.flush_dataset() # this (after a while) slows down the simulation considerably
            
        # set the right parcels
        #parcels = agent_set.compute_variables(["household.disaggregate(building.parcel_id)"],
        #                                      dataset_pool = self.dataset_pool)
        #agent_set.modify_attribute(name="parcel_id", data = parcels)
