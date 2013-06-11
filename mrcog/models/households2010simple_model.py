# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, unique
from opus_core.logger import logger
from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel
from opus_core.session_configuration import SessionConfiguration

class Households2010Model(HouseholdLocationChoiceModel):
    model_name = "HouseholdAllocationtoBuildingModel"
    model_short_name = "HATBM"
        
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):

        dataset_pool = SessionConfiguration().get_dataset_pool()
        #county_set = dataset_pool.get_dataset('county')
        building_set = dataset_pool.get_dataset('building')
        #building_set.add_attribute(name='submarket', data=building_set.compute_variables('bayarea.building.submarket_id'))

        
        household_zonetype = agent_set.compute_variables("((1000000 * (household.county_id == 1) + 2000000*(household.county_id==43) + 3000000*(household.county_id==49) + 4000000*(household.county_id==57) + 5000000 * (household.county_id==61)) + household.tract_id).astype('i4')")
        
        building_zonetype = building_set.compute_variables("((100 * building.disaggregate(parcel.tract_id)) + (1000000*building.disaggregate(parcel.county_id))).astype('i4')")
        
        agent_set.add_primary_attribute(name='zonetype', data=household_zonetype)
        
        building_set.add_primary_attribute(name='zonetype', data=building_zonetype)
        
        
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
            
            
        # agents_index = where(agent_set.get_attribute("building_id") < 1)[0]
        # #agents_index = arange(agent_set.size())
        # cond_array = zeros(agent_set.size(), dtype="bool8")
        # cond_array[agents_index] = True
        # #county_ids = county_set.get_id_attribute()
        # #household_unplaced = agent_set.compute_variables("(household.building_id<1).astype('i4')")
        # agents_zonetypes = agent_set.get_attribute('zone_id')
        # #agents_zonetypes = agents_zonetypes*household_unplaced
        # zonetype_ids = unique(building_set.get_attribute('zone_id'))#unique(agents_zonetypes)
        # for zonetype_id in zonetype_ids:
            # new_index = where(logical_and(cond_array, agents_zonetypes == zonetype_id))[0]
            # self.filter = "building.zone_id == %s" % zonetype_id
            # logger.log_status("HLCM for zone %s" % zonetype_id)
            # logger.log_status("HLCM for households %s" % agent_set['household_id'][new_index])
            # HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             # agents_index=new_index, **kwargs)
            # agent_set.flush_dataset()
            # #self.choice_set.flush_dataset() # this (after a while) slows down the simulation considerably
            
            
        household_county = agent_set.compute_variables("((1 * (household.county_id == 1) + 2*(household.county_id==43) + 3*(household.county_id==49) + 4*(household.county_id==57) + 5 * (household.county_id==61))).astype('i4')")
        
        building_county = building_set.compute_variables("(building.disaggregate(parcel.county_id)).astype('i4')")
        
        agent_set.add_primary_attribute(name='county', data=household_county)
        
        building_set.add_primary_attribute(name='county', data=building_county)
        
        parcel_set = dataset_pool.get_dataset('parcel')
        
        agents_index = where(agent_set.get_attribute("building_id") < 1)[0]
        #agents_index = arange(agent_set.size())
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        #county_ids = county_set.get_id_attribute()
        #household_unplaced = agent_set.compute_variables("(household.building_id<1).astype('i4')")
        agents_zonetypes = agent_set.get_attribute('county')
        #agents_zonetypes = agents_zonetypes*household_unplaced
        zonetype_ids = unique(parcel_set.get_attribute('county_id'))#unique(agents_zonetypes)
        for zonetype_id in zonetype_ids:
            new_index = where(logical_and(cond_array, agents_zonetypes == zonetype_id))[0]
            self.filter = "building.county == %s" % zonetype_id
            logger.log_status("HLCM for zone %s" % zonetype_id)
            logger.log_status("HLCM for households %s" % agent_set['household_id'][new_index])
            HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             agents_index=new_index, **kwargs)
            agent_set.flush_dataset()
            
        # set the right parcels
        #parcels = agent_set.compute_variables(["household.disaggregate(building.parcel_id)"],
        #                                      dataset_pool = self.dataset_pool)
        #agent_set.modify_attribute(name="parcel_id", data = parcels)
