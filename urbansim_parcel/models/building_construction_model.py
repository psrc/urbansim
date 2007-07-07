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
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from opus_core.logger import logger
from opus_core.misc import unique_values
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import DatasetSubset

from numpy import where, arange, resize, array, cumsum, concatenate

class BuildingConstructionModel(Model):
    """Process any pre-scheduled development projects (those that have status 'active'). New buildings are 
    created according to the corresponding velocity function. The velocity function dataset is taken from dataset_pool.
    """
    model_name = "BuildingConstructionModel"

    def run (self, development_proposal_set, building_dataset, dataset_pool):
        if development_proposal_set.size() <= 0:
            logger.log_status("Proposal set is empty. Nothing to be constructed.")
            return development_proposal_set
        
        # load velocity function dataset
        try:
            velocity_function_set = dataset_pool.get_dataset("velocity_function_dataset")
        except:
            velocity_function_set = None
                
        # choose active projects
        active_idx = where(development_proposal_set.get_attribute("status_id") == development_proposal_set.id_active)[0]
        if active_idx.size <= 0:
            logger.log_status("No new buildings built.")
            return development_proposal_set
        
        active_proposal_set = DatasetSubset(development_proposal_set, active_idx)
        
        # create proposal_component_set from the active proposals
        proposal_component_set = create_from_proposals_and_template_components(active_proposal_set, 
                                                   dataset_pool.get_dataset('development_template_component'))
        dataset_pool.replace_dataset(proposal_component_set.get_dataset_name(), proposal_component_set)
        
        # determine building types and corresponding unit names of the involved building_types
        building_type_id = proposal_component_set.get_attribute("building_type_id")
        building_type_set = dataset_pool.get_dataset("building_type")
#        unit_names = building_type_set.compute_variables([
#                                  'building_type.disaggregate(generic_building_type.unit_name)'], dataset_pool=dataset_pool)
        unit_names = building_type_set.get_attribute("unit_name")
        # get unique values of the involved generic building types and unique unit names
        unique_building_types = unique_values(building_type_id)
        index_in_building_types = building_type_set.get_id_index(unique_building_types)
        unit_names = unit_names[index_in_building_types]
        unique_unit_names = unique_values(unit_names)
        
        # determine existing units on parcels
        parcels = dataset_pool.get_dataset("parcel")
        parcels.compute_variables(map(lambda x: "%s = parcel.aggregate(urbansim_parcel.building.%s)" % (x, x), unique_unit_names), 
                                  dataset_pool=dataset_pool)
        parcel_is_lut_vacant = parcels.compute_variables(["urbansim_parcel.parcel.is_land_use_type_vacant"], 
                                  dataset_pool=dataset_pool)
        parcel_lut = parcels.get_attribute("land_use_type_id")
        component_land_use_types = proposal_component_set.compute_variables([
              'development_project_proposal_component.disaggregate(development_template.land_use_type_id, [development_project_proposal])'],
                      dataset_pool=dataset_pool)
        # from the velocity function determine the amount to be built for each component
        if velocity_function_set is not None:
            development_amount = proposal_component_set.compute_variables(["cummulative_amount_of_development"], 
                                                                      dataset_pool=dataset_pool)
        else: # if there is no velocity function, all components have velocity of 100%
            development_amount = resize(array([100], dtype="int32"), proposal_component_set.size())
        
        # amount to be built
        to_be_built = proposal_component_set.compute_variables([
                    'urbansim_parcel.development_project_proposal_component.units_proposed'],
                                                 dataset_pool=dataset_pool)/100.0 * development_amount
        
        # initializing for new buildings
        max_building_id = building_dataset.get_id_attribute().max()
        new_buildings = {}
        new_buildings["parcel_id"] = array([], dtype="int32")
        new_buildings["residential_units"] = array([], dtype="int32")
        new_buildings["non_residential_sqft"] = array([], dtype="int32")
        new_buildings["building_type_id"] = array([], dtype="int32")
        new_buildings["sqft_per_unit"] = array([], dtype=building_dataset.get_attribute("sqft_per_unit").dtype)
        new_buildings["land_area"] = array([], dtype=building_dataset.get_attribute("land_area").dtype)
        
        sqft_per_unit = proposal_component_set.get_attribute("building_sqft_per_unit").astype(new_buildings["sqft_per_unit"].dtype)
        parcel_sqft = parcels.get_attribute("parcel_sqft").astype(new_buildings["land_area"].dtype)
        
        # iterate over building types that are unique over the involved proposals
        for itype in range(unique_building_types.size):
            this_building_type = unique_building_types[itype]
            unit_name = unit_names[itype]
            component_index = where(building_type_id == this_building_type)[0]
            parcel_ids_in_components = proposal_component_set.get_attribute_by_index("parcel_id", component_index)
            unique_parcels = unique_values(parcel_ids_in_components)
            # iterate over involved parcels
            for parcel_id in unique_parcels:
                pidx = component_index[parcel_ids_in_components==parcel_id]
                parcel_index = parcels.get_id_index(parcel_id)
                # what is already built on this parcel
                amount_built = parcels.get_attribute_by_index(unit_name, parcel_index)
                # what is proposed on this parcel
                amount_proposed = to_be_built[pidx].sum()
                # build if needed
                if amount_proposed > amount_built:
                    if unit_name == "residential_units":
                        bunit = "residential_units"
                        bnunit = "non_residential_sqft"
                    else:
                        bnunit = "residential_units"
                        bunit = "non_residential_sqft"
                    to_be_built_cumsum = cumsum(to_be_built[pidx])
                    idx_to_be_built = where(to_be_built_cumsum > amount_built)[0]
                    new_buildings["parcel_id"] = concatenate((new_buildings["parcel_id"], 
                                                              array(idx_to_be_built.size * [parcel_id])))
                    new_buildings[bunit] = concatenate((new_buildings[bunit], to_be_built[pidx][idx_to_be_built]))
                    new_buildings[bnunit] = concatenate((new_buildings[bnunit], array(idx_to_be_built.size * [0])))
                    new_buildings["building_type_id"] = concatenate((new_buildings["building_type_id"], 
                             array(idx_to_be_built.size * [this_building_type])))
                    new_buildings["sqft_per_unit"] = concatenate((new_buildings["sqft_per_unit"],
                                                                  sqft_per_unit[pidx][idx_to_be_built]))
                    new_buildings["land_area"] = concatenate((new_buildings["land_area"], 
                                                              array(idx_to_be_built.size * [parcel_sqft[parcel_index]])))
                    if parcel_is_lut_vacant[parcel_index]:
                        parcel_lut[parcel_index] = component_land_use_types[pidx][idx_to_be_built][0]
                                                                  
        # add created buildings to the existing building dataset
        new_buildings["building_id"] = max_building_id + arange(1, new_buildings["parcel_id"].size+1)
        new_buildings['year_built'] = resize(array([SimulationState().get_current_time()], dtype="int32"), 
                                             new_buildings["parcel_id"].size)
        building_dataset.add_elements(new_buildings, require_all_attributes=False)
        if "zone_id" in building_dataset.get_known_attribute_names():
            zone_ids = building_dataset.compute_variables(['building.disaggregate(parcel.zone_id)'], dataset_pool=dataset_pool)
            building_dataset.modify_attribute(name="zone_id", data=zone_ids)
        if "county" in building_dataset.get_known_attribute_names():
            county_ids = building_dataset.compute_variables(['building.disaggregate(parcel.county)'], dataset_pool=dataset_pool)
            building_dataset.modify_attribute(name="county", data=county_ids)
        
        logger.log_status("%s new buildings built." % new_buildings["parcel_id"].size)
        # remove active proposals from the proposal set
        development_proposal_set.remove_elements(active_idx)
        return development_proposal_set