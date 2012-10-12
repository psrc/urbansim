# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, array, unique
from numpy.random import shuffle
from opus_core.logger import logger
from urbansim.models.real_estate_transition_model import RealEstateTransitionModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.building_dataset import BuildingDataset

class RealEstateTransitionModelBySubmarkets(RealEstateTransitionModel):

    def run(self):
        dataset_pool = SessionConfiguration().get_dataset_pool()
        current_year = SimulationState().get_current_time()
        building_set = dataset_pool.get_dataset('building')
        parcel_set = dataset_pool.get_dataset('parcel')
        proposal_set = dataset_pool.get_dataset('proposed_development_event')
        attribs = proposal_set.get_known_attribute_names()
        parcels = proposal_set.get_attribute('parcel_id')
        amount = proposal_set.get_attribute('amount')
        year = proposal_set.get_attribute('year')
        proposal_in_current_year = (year==current_year)
        building_type_id = proposal_set.get_attribute('building_type_id')
        proposed_sf_units = amount * (building_type_id == 1)*proposal_in_current_year
        proposed_townhome_units = amount * (building_type_id == 2)*proposal_in_current_year
        proposed_mf_units = amount * (building_type_id == 3)*proposal_in_current_year
        proposal_zone = proposal_in_current_year * proposal_set.compute_variables('_proposal_zone = proposed_development_event.disaggregate(parcel.zone_id)')
        parcel_zone = parcel_set.get_attribute('zone_id')
        zone_ids = unique(parcel_zone)
        in_zone = None
        for zone_id in zone_ids:
            proposals_in_zone = where(proposal_zone==zone_id)[0]
            logger.log_status("proposals_in_zone %s: %s" % (zone_id,proposals_in_zone.size))
            if proposals_in_zone.size > 0:
                logger.log_status("sf units in zone %s: %s" % (zone_id,proposed_sf_units[proposals_in_zone].sum()))
                logger.log_status("townhome units in zone %s: %s" % (zone_id,proposed_townhome_units[proposals_in_zone].sum()))
                logger.log_status("mf units in zone %s: %s" % (zone_id,proposed_mf_units[proposals_in_zone].sum()))
            # if in_zone is not None:
                # building_set.delete_computed_attributes()
                # parcel_set.delete_computed_attributes()
            # in_zone = building_set.compute_variables('_in_zone = building.disaggregate(parcel.zone_id)==%s'% (zone_id))
            # idx_in_zone = where(in_zone)[0]
            # max_building_id = (building_set.get_attribute('building_id')).max()
            # attribs = building_set.get_known_attribute_names()
            # table_data={}
            # for name in attribs:
                # table_data["%s"%(name)]=building_set.get_attribute("%s" %(name))[idx_in_zone]
            # storage = StorageFactory().get_storage('dict_storage')
            # table_name = 'buildings_zone'
            # storage.write_table(
                # table_name=table_name,
                # table_data=table_data
                # )
            # buildings_zone = BuildingDataset(in_storage=storage, in_table_name=table_name)
            # if buildings_zone.size() > 0:
                # dptm = RealEstateTransitionModel(target_vancy_dataset=dataset_pool.get_dataset('target_vacancy'))
                # results, index = dptm.run(realestate_dataset = buildings_zone,
                                   # year = current_year,
                                   # occupied_spaces_variable = 'occupied_spaces',
                                   # total_spaces_variable = 'total_spaces',
                                   # target_attribute_name = 'target_vacancy_rate',
                                   # sample_from_dataset = dataset_pool.get_dataset('building'),
                                   # dataset_pool=dataset_pool,
                                   # append_to_realestate_dataset = False,
                                   # reset_attribute_value={'parcel_id':-1},
                                   # sample_filter="(building.building_type_id==1)*(building.year_built>1989) +  (building.building_type_id==3)*(building.year_built>1979) +  (building.building_type_id==2)*(building.year_built>1989)+ (building.building_type_id>3)*(building.building_type_id<12)"
                                   # )
                # #This is where, now that we know the demand for sqft, I'd want to insert the appropriate amount of permitted/proposed projects.
                # if results is not None:
                    # results.modify_attribute('year_built', array(index.size*[current_year]))
                    # attribs2 = results.get_known_attribute_names()
                    # table_data2={}
                    # for name in attribs2:
                        # if name in attribs:
                            # table_data2["%s"%(name)]=results.get_attribute("%s" %(name))
                    # building_set.add_elements(data=table_data2, require_all_attributes=False, change_ids_if_not_unique=True)

                    # index_new_sf_units = where(logical_and(building_set['building_id']>max_building_id, building_set['building_type_id']==1))[0]
                    # index_new_mf_units = where(logical_and(building_set['building_id']>max_building_id, (building_set['building_type_id']==2)+(building_set['building_type_id']==3)))[0]
                    # index_new_industrial_units = where(logical_and(building_set['building_id']>max_building_id, (building_set['building_type_id']==6)+(building_set['building_type_id']==7)))[0]
                    # index_new_commercial_units = where(logical_and(building_set['building_id']>max_building_id, (building_set['building_type_id']==9)+(building_set['building_type_id']==8)))[0]
                    # if index_new_sf_units.size > 0:
                        # for building in index_new_sf_units:
                            # has_available_sf_capacity = parcel_set.compute_variables('_has_available_sf_capacity = (parcel.zone_id==%s) * parcel.disaggregate(zoning.allow_sf==1) * (((safe_array_divide(parcel.parcel_sqft,parcel.disaggregate(zoning.min_lot_size)).round().astype(int32)) - (parcel.number_of_agents(building)))>0)'%(zone_id))
                            # idx_has_available_sf_capacity = where(has_available_sf_capacity)[0]
                            # if idx_has_available_sf_capacity.size < 1:
                                # logger.log_status("No more single-family capacity remaining in this zone")
                                # break
                            # parcel_ids_available_sf_capacity=(parcel_set.get_attribute('parcel_id'))[idx_has_available_sf_capacity]
                            # shuffle(parcel_ids_available_sf_capacity)
                            # parcel_id_to_assign = parcel_ids_available_sf_capacity[:1]
                            # building_set.modify_attribute('parcel_id', parcel_id_to_assign, building)
                    # if index_new_commercial_units.size > 0:
                        # for building in index_new_commercial_units:
                            # available_commercial_capacity = parcel_set.compute_variables('_available_commercial_capacity = (parcel.zone_id==%s) * parcel.disaggregate(zoning.allow_comm==1) * clip_to_zero((((parcel.parcel_sqft)*parcel.disaggregate(zoning.max_far)).round().astype(int32)-(parcel.aggregate(1000*building.residential_units))) - (parcel.aggregate(building.non_residential_sqft)))'%(zone_id))
                            # ####update the capacity calcs to account for sqft per unit of hotel/resort units
                            # building_sqft = building_set['non_residential_sqft'][building]
                            # idx_building_would_fit = where(available_commercial_capacity>=building_sqft)[0]
                            # if idx_building_would_fit.size < 1:
                                # logger.log_status("No more commercial capacity remaining in this zone")
                                # break
                            # parcel_ids_with_enough_capacity = (parcel_set.get_attribute('parcel_id'))[idx_building_would_fit]
                            # shuffle(parcel_ids_with_enough_capacity) #replace with code involving random/uniform/cumprob/searchsorted etc...  I think it would be faster
                            # parcel_id_to_assign = parcel_ids_with_enough_capacity[:1]
                            # building_set.modify_attribute('parcel_id', parcel_id_to_assign, building)
                    # if index_new_industrial_units.size > 0:
                        # for building in index_new_industrial_units:
                            # available_industrial_capacity = parcel_set.compute_variables('_available_industrial_capacity = (parcel.zone_id==%s) * parcel.disaggregate(zoning.allow_indust==1) * clip_to_zero((((parcel.parcel_sqft)*parcel.disaggregate(zoning.max_far)).round().astype(int32)-(parcel.aggregate(1000*building.residential_units))) - (parcel.aggregate(building.non_residential_sqft)))'%(zone_id))
                            # building_sqft = building_set['non_residential_sqft'][building]
                            # idx_building_would_fit = where(available_industrial_capacity>=building_sqft)[0]
                            # if idx_building_would_fit.size < 1:
                                # logger.log_status("No more industrial capacity remaining in this zone")
                                # break
                            # parcel_ids_with_enough_capacity = (parcel_set.get_attribute('parcel_id'))[idx_building_would_fit]
                            # shuffle(parcel_ids_with_enough_capacity) 
                            # parcel_id_to_assign = parcel_ids_with_enough_capacity[:1]
                            # building_set.modify_attribute('parcel_id', parcel_id_to_assign, building)
                    # if index_new_mf_units.size > 0:
                        # for building in index_new_mf_units:
                            # available_mf_capacity = parcel_set.compute_variables('_available_mf_capacity = (parcel.zone_id==%s) * parcel.disaggregate(zoning.allow_mf==1) * clip_to_zero(((((parcel.parcel_sqft)*parcel.disaggregate(zoning.max_far)).round().astype(int32)) - (parcel.aggregate(building.non_residential_sqft)))/1000 - (parcel.aggregate(building.residential_units)))'%(zone_id))
                            # building_resunits = building_set['residential_units'][building]
                            # idx_building_would_fit = where(available_mf_capacity>=building_resunits)[0]
                            # if idx_building_would_fit.size < 1:
                                # logger.log_status("No more multifamily capacity remaining in this zone")
                                # break
                            # parcel_ids_with_enough_capacity = (parcel_set.get_attribute('parcel_id'))[idx_building_would_fit] 
                            # shuffle(parcel_ids_with_enough_capacity)
                            # parcel_id_to_assign = parcel_ids_with_enough_capacity[:1]
                            # building_set.modify_attribute('parcel_id', parcel_id_to_assign, building)
                    # index_unplaced_buildings = where(logical_and(building_set['building_id']>max_building_id, building_set['parcel_id']<=0))[0]
                    # logger.log_status("Number of unplaced buildings to be removed from zone%s: %s" % (zone_id,index_unplaced_buildings.size))
                    # building_set.remove_elements(index_unplaced_buildings)