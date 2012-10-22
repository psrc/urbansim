# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model import Model
from numpy import arange, zeros, logical_and, where, array, unique, ones
from numpy.random import randint, shuffle
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration

class Household2010AllocationModel(Model):
    """
    """
    model_name = "Allocating Zonal Households Model"

    def run(self):

        dataset_pool = SessionConfiguration().get_dataset_pool()
        household_set = dataset_pool.get_dataset('household')
        building_set = dataset_pool.get_dataset('building')
        parcel_set = dataset_pool.get_dataset('parcel')

        idx_all_hh = where(household_set.compute_variables('household.household_id > 0'))[0]
        household_set.modify_attribute('building_id', array(idx_all_hh.size*[-1]), idx_all_hh)

        zone_ids = household_set.get_attribute('household_zone')
        zone_ids = unique(zone_ids)
        for zone_id in zone_ids:
            logger.log_status("ZONE: %s" % (zone_id) )
            parcel_set.delete_computed_attributes()
            building_set.delete_computed_attributes()
            household_set.delete_computed_attributes()
            idx_households_to_place = where(household_set['household_zone'] == zone_id)[0]
            for household in idx_households_to_place:
                household_building_type = household_set['building_type_id'][household]
                available_hh_capacity = building_set.compute_variables('_available_hh_capacity_type = (building.disaggregate(parcel.zone_id) == %s) * ((building.residential_units)>building.number_of_agents(household)) * (building.building_type_id == %s)'%(zone_id,household_building_type))
                idx_available_hh_capacity = where(available_hh_capacity)[0]
                if idx_available_hh_capacity.size < 1:
                    available_hh_capacity = building_set.compute_variables('_available_hh_capacity = (building.disaggregate(parcel.zone_id) == %s) * ((building.residential_units)>building.number_of_agents(household)) * (building.building_type_id<4)'%(zone_id))
                    idx_available_hh_capacity = where(available_hh_capacity)[0]
                    if idx_available_hh_capacity.size < 1:
                        logger.log_status("No residential capacity remaining in zone %s"%(zone_id))
                        building_in_zone = building_set.compute_variables('(building.disaggregate(parcel.zone_id)==%s)*(building.building_type_id<4)'%(zone_id))
                        idx_building = where(building_in_zone)[0]
                        if idx_building.size < 1:
                            logger.log_status("No residential buildings in zone %s, but hh need to be placed.  Adding one SF unit."%(zone_id))
                            building_to_add = {}
                            building_to_add['building_type_id'] = array([1])
                            building_to_add['non_residential_sqft'] = array([0])
                            building_to_add['residential_units'] = array([1])
                            building_to_add['hotel_units'] = array([0])
                            building_to_add['resort_units'] = array([0])
                            building_to_add['stories'] = array([1])
                            building_to_add['sqft_per_unit'] = array([1000])
                            building_to_add['year_built'] = array([2010])
                            parcel_in_zone = parcel_set.compute_variables('_parcel_in_zone = (parcel.zone_id==%s)'%(zone_id))
                            idx_parcel = where(parcel_in_zone)[0]
                            parcel_ids_in_zone=(parcel_set.get_attribute('parcel_id'))[idx_parcel]
                            shuffle(parcel_ids_in_zone)
                            parcel_id_to_assign = parcel_ids_in_zone[:1]
                            building_to_add['parcel_id'] = parcel_id_to_assign
                            building_set.add_elements(data=building_to_add, require_all_attributes=False, change_ids_if_not_unique=True)
                            building_in_zone = building_set.compute_variables('(building.disaggregate(parcel.zone_id)==%s)'%(zone_id))
                            idx_building = where(building_in_zone)[0]
                        building_ids_in_zone=(building_set.get_attribute('building_id'))[idx_building]
                        shuffle(building_ids_in_zone)
                        building_id_to_assign = building_ids_in_zone[:1]
                        household_set.modify_attribute('building_id', building_id_to_assign, household)
                    else:
                        building_ids_with_enough_capacity = (building_set.get_attribute('building_id'))[idx_available_hh_capacity] 
                        shuffle(building_ids_with_enough_capacity)
                        building_id_to_assign = building_ids_with_enough_capacity[:1]
                        household_set.modify_attribute('building_id', building_id_to_assign, household)
                else:
                    building_ids_with_enough_capacity = (building_set.get_attribute('building_id'))[idx_available_hh_capacity] 
                    shuffle(building_ids_with_enough_capacity)
                    building_id_to_assign = building_ids_with_enough_capacity[:1]
                    household_set.modify_attribute('building_id', building_id_to_assign, household)

        household_dpa = household_set.compute_variables('household.disaggregate(parcel.dpa_id,intermediates=[building])')
        household_set.modify_attribute('dpa_id', household_dpa)
