# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, array, logical_and
from numpy.random import shuffle
from opus_core.logger import logger
from urbansim.models.real_estate_transition_model import RealEstateTransitionModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState

class RealEstateTransitionModelBySubmarkets(RealEstateTransitionModel):

    def run(self):

        dataset_pool = SessionConfiguration().get_dataset_pool()
        submarket_set = dataset_pool.get_dataset('submarket')
        building_set = dataset_pool.get_dataset('building')
        parcel_set = dataset_pool.get_dataset('parcel')
        current_year = SimulationState().get_current_time()
        dptm = RealEstateTransitionModel(target_vancy_dataset=dataset_pool.get_dataset('target_vacancy'))
        results, index = dptm.run(realestate_dataset = dataset_pool.get_dataset('building'),
                           year = current_year,
                           occupied_spaces_variable = 'occupied_spaces',
                           total_spaces_variable = 'total_spaces',
                           target_attribute_name = 'target_vacancy_rate',
                           sample_from_dataset = dataset_pool.get_dataset('building'),
                           dataset_pool=dataset_pool,
                           append_to_realestate_dataset = True,
                           reset_attribute_value={'parcel_id':-1},
                           sample_filter="(building.building_type_id==1)*(building.year_built>1989) +  (building.building_type_id==3)*(building.year_built>1979) +  (building.building_type_id==2)*(building.year_built>1989)+ (building.building_type_id>3)*(building.building_type_id<12)"
                           #year_built = 2001,
                           #table_name = 'buildings',
                           #dataset_name = 'building',
                           #id_name = 'building_id'
                           )
        #This is where, now that we know the demand for sqft, I'd want to insert the appropriate amount of permitted/proposed projects.
        building_set.modify_attribute('year_built', array(index.size*[current_year]), index)
        minimum_new_building_id = (building_set.get_attribute('building_id'))[index].min()
        max_old_building_id = minimum_new_building_id - 1
        index_new_sf_units = where(logical_and(building_set['building_id']>max_old_building_id, building_set['building_type_id']==1))[0]
        #Come up with a random list of eligible parcel_id's of length index_new_sf_units, then assign these parcel_id's to this index of buildings
        has_available_sf_capacity = parcel_set.compute_variables('_has_available_sf_capacity = parcel.disaggregate(zoning.allow_sf==1) * (((safe_array_divide(parcel.parcel_sqft,parcel.disaggregate(zoning.min_lot_size)).round().astype(int32)) - (parcel.number_of_agents(building)))>0)')
        idx_has_available_sf_capacity = where(has_available_sf_capacity)[0]
        parcel_ids_available_sf_capacity=(parcel_set.get_attribute('parcel_id'))[idx_has_available_sf_capacity]
        shuffle(parcel_ids_available_sf_capacity)
        parcel_ids_to_assign = parcel_ids_available_sf_capacity[:index_new_sf_units.size]
        building_set.modify_attribute('parcel_id', parcel_ids_to_assign, index_new_sf_units)
        #remember at the end of this program to delete all buildings with parcel_id of -1.  These buildings should not be placed because zoning is maxed out (e.g. sf detached will prolly be maxed after 10 yr...)
        index_new_mf_units = where(logical_and(building_set['building_id']>max_old_building_id, (building_set['building_type_id']==2)+(building_set['building_type_id']==3)))[0]
        index_new_industrial_units = where(logical_and(building_set['building_id']>max_old_building_id, (building_set['building_type_id']==6)+(building_set['building_type_id']==7)))[0]
        index_new_commercial_units = where(logical_and(building_set['building_id']>max_old_building_id, (building_set['building_type_id']==9)+(building_set['building_type_id']==8)))[0]
        for building in index_new_commercial_units:
            available_commercial_capacity = parcel_set.compute_variables('_available_commercial_capacity = parcel.disaggregate(zoning.allow_comm==1) * clip_to_zero((((parcel.parcel_sqft)*parcel.disaggregate(zoning.max_far)).round().astype(int32)-(parcel.aggregate(1000*building.residential_units))) - (parcel.aggregate(building.non_residential_sqft)))')
            building_sqft = building_set['non_residential_sqft'][building]
            idx_building_would_fit = where(available_commercial_capacity>=building_sqft)[0]
            parcel_ids_with_enough_capacity = (parcel_set.get_attribute('parcel_id'))[idx_building_would_fit]
            shuffle(parcel_ids_with_enough_capacity) #replace with code involving random/uniform/cumprob/searchsorted etc...  I think it would be faster
            parcel_id_to_assign = parcel_ids_with_enough_capacity[:1] #WHAT TO DO WITH THERE ARE NO PARCELS WITH CAPACITY?!?
            building_set.modify_attribute('parcel_id', parcel_id_to_assign, building)
        for building in index_new_industrial_units:
            available_industrial_capacity = parcel_set.compute_variables('_available_industrial_capacity = parcel.disaggregate(zoning.allow_indust==1) * clip_to_zero((((parcel.parcel_sqft)*parcel.disaggregate(zoning.max_far)).round().astype(int32)-(parcel.aggregate(1000*building.residential_units))) - (parcel.aggregate(building.non_residential_sqft)))')
            building_sqft = building_set['non_residential_sqft'][building]
            idx_building_would_fit = where(available_industrial_capacity>=building_sqft)[0]
            parcel_ids_with_enough_capacity = (parcel_set.get_attribute('parcel_id'))[idx_building_would_fit]
            shuffle(parcel_ids_with_enough_capacity) #replace with code involving random/uniform/cumprob/searchsorted etc...  I think it would be faster
            parcel_id_to_assign = parcel_ids_with_enough_capacity[:1]
            building_set.modify_attribute('parcel_id', parcel_id_to_assign, building)
        for building in index_new_mf_units:
            available_mf_capacity = parcel_set.compute_variables('_available_mf_capacity = parcel.disaggregate(zoning.allow_mf==1) * clip_to_zero(((((parcel.parcel_sqft)*parcel.disaggregate(zoning.max_far)).round().astype(int32)) - (parcel.aggregate(building.non_residential_sqft)))/1000 - (parcel.aggregate(building.residential_units)))')
            building_resunits = building_set['residential_units'][building]
            idx_building_would_fit = where(available_mf_capacity>=building_resunits)[0]
            parcel_ids_with_enough_capacity = (parcel_set.get_attribute('parcel_id'))[idx_building_would_fit]
            shuffle(parcel_ids_with_enough_capacity) #replace with code involving random/uniform/cumprob/searchsorted etc...  I think it would be faster
            parcel_id_to_assign = parcel_ids_with_enough_capacity[:1]
            building_set.modify_attribute('parcel_id', parcel_id_to_assign, building)
        index_unplaced_buildings = where(logical_and(building_set['building_id']>max_old_building_id, building_set['parcel_id']<=0))[0]
        logger.log_status("Number of unplaced buildings to be removed: %s" % (index_unplaced_buildings.size))
        building_set.remove_elements(index_unplaced_buildings)






    # def run(self, realestate_dataset,
            # year=None, 
            # occupied_spaces_variable="occupied_units",
            # total_spaces_variable="total_units",
            # target_attribute_name='target_vacancy_rate',
            # sample_from_dataset = None,
            # sample_filter="",
            # reset_attribute_value={}, 
            # year_built = 'year_built',
            # dataset_pool=None,
            # append_to_realestate_dataset = False,
            # table_name = "development_projects",
            # dataset_name = "development_project",
            # id_name = 'development_project_id',
            # **kwargs):
        
    # def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):

        # dataset_pool = SessionConfiguration().get_dataset_pool()
        # submarket_set = dataset_pool.get_dataset('submarket')
        # building_set = dataset_pool.get_dataset('building')
        # building_set.add_attribute(name='submarket', data=building_set.compute_variables('honolulu_parcel.building.submarket_id'))

        # if agents_index is None:
            # agents_index = arange(agent_set.size())
        # cond_array = zeros(agent_set.size(), dtype="bool8")
        # cond_array[agents_index] = True
        # submarket_ids = submarket_set.get_id_attribute()
        # agents_submarkets = agent_set.get_attribute(submarket_set.get_id_name()[0])
        # for submarket_id in submarket_ids:
            # new_index = where(logical_and(cond_array, agents_submarkets == submarket_id))[0]
            # self.filter = "building.submarket == %s" % submarket_id
            # logger.log_status("HLCM for submarket %s" % submarket_id)
            # HouseholdLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             # agents_index=new_index, **kwargs)
            # agent_set.flush_dataset()
            #self.choice_set.flush_dataset() # this (after a while) slows down the simulation considerably
            
        # set the right parcels
        #parcels = agent_set.compute_variables(["household.disaggregate(building.parcel_id)"],
        #                                      dataset_pool = self.dataset_pool)
        #agent_set.modify_attribute(name="parcel_id", data = parcels)
