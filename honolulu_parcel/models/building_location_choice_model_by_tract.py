# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, array, unique
from opus_core.logger import logger
from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel
from opus_core.session_configuration import SessionConfiguration

class BuildingLocationChoiceModelByTract(HouseholdLocationChoiceModel):
        
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):

        dataset_pool = SessionConfiguration().get_dataset_pool()
        #submarket_set = dataset_pool.get_dataset('employment_submarket')
        building_set = dataset_pool.get_dataset('building')
        parcel_set = dataset_pool.get_dataset('parcel')
        building_tract = building_set.get_attribute('neighborhood_board_id')
        building_parcel_id = building_set.get_attribute('parcel_id')
        agents_index = where(building_parcel_id<1)[0]
        if agents_index is None:
            agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        census_tracts = parcel_set.get_attribute('neighborhood_board_id')
        census_tracts = unique(census_tracts)
        #agents_submarkets = agent_set.get_attribute(submarket_set.get_id_name()[0])
        for tract_id in census_tracts:
            new_index = where(logical_and(cond_array, building_tract == tract_id))[0]
            self.filter = "parcel.neighborhood_board_id == %s" % tract_id
            logger.log_status("Building allocation to parcel for census tract %s" % tract_id)
            HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            #self.choice_set.flush_dataset() # this (after a while) slows down the simulation considerably
            
        # set the right parcels
        #parcels = agent_set.compute_variables(["household.disaggregate(building.parcel_id)"],
        #                                      dataset_pool = self.dataset_pool)
        #agent_set.modify_attribute(name="parcel_id", data = parcels)
