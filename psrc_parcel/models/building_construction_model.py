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
from psrc_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from opus_core.logger import logger
from opus_core.misc import unique_values
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import DatasetSubset

from numpy import where, arange, resize

class BuildingConstructionModel(Model):
    """Process any pre-scheduled development projects (those that have status 'active'). New buildings are 
    created according to the corresponding velocity function. The velocity function dataset is taken from dataset_pool.
    """
    model_name = "BuildingConstructionModel"

    def run (self, development_proposal_set, building_dataset, dataset_pool):
        # load velocity function dataset
        try:
            velocity_function_set = dataset_pool.get_dataset("velocity_function_dataset")
        except:
            velocity_function_set = None
                
        # choose active projects
        active_idx = where(development_proposal_set.get_attribute("status_id") == development_proposal_set.id_active)[0]
        active_proposal_set = DatasetSubset(development_proposal_set, active_idx)
        
        # create proposal_component_set from the active proposals
        proposal_component_set = create_from_proposals_and_template_components(active_proposal_set, 
                                                   dataset_pool.get_dataset('development_template_component'))
        dataset_pool.replace_dataset(proposal_component_set.get_dataset_name(), proposal_component_set)
        
        # determine generic building types and corresponding unit names of the involved building_types
        generic_building_type_id = proposal_component_set.compute_variables([
        'generic_building_type_id = development_project_proposal_component.disaggregate(building_type.generic_building_type_id)'],
                                                 dataset_pool=dataset_pool)
        generic_building_type_set = dataset_pool.get_dataset("generic_building_type")
        
        # get unique values of the involved generic building types and unique unit names
        unique_building_types = unique_values(generic_building_type_id)
        index_in_gen_building_types = generic_building_type_set.get_id_index(unique_building_types)
        unit_names = generic_building_type_set.get_attribute_by_index("unit_name", index_in_gen_building_types)
        unique_unit_names = unique_values(unit_names)
        
        # determine existing units on parcels
        parcels = dataset_pool.get_dataset("parcel")
        parcels.compute_variables(map(lambda x: "%s = parcel.aggregate(building.%s)" % (x, x), unique_unit_names), 
                                  dataset_pool=dataset_pool)
        
        # from the velocity function determine the amount to be built for each component
        if velocity_function is not None:
            development_amount = proposal_component_set.compute_variables(["cummulative_amount_of_development"], 
                                                                      dataset_pool=dataset_pool)
        else: # if there is no velocity function, all components have velocity of 100%
            development_amount = resize(array([100], dtype="int32"), proposal_component_set.size)
        
        # amount to be built
        to_be_built = proposal_component_set.get_attribute('units_proposed')/100.0 * development_amount
        
        # initializing for new buildings
        max_building_id = building_dataset.get_id_attribute().max()
        new_buildings = {}
        new_buildings["parcel_id"] = []
        new_buildings["residential_units"] = []
        new_buildings["non_residential_sqft"] = []
        
        # iterate over building types that are unique over the involved proposals
        for itype in range(unique_building_types.size):
            this_gbuilding_type = unique_building_types[itype]
            unit_name = unit_names[itype]
            component_index = where(generic_building_type_id == this_gbuilding_type)[0]
            parcel_ids_in_components = proposal_component_set.get_attribute_by_index("parcel_id", component_index)
            unique_parcels = unique_values(parcel_ids_in_components)
            # iterate over involved parcels
            for parcel_id in unique_parcels:
                pidx = component_index[parcel_ids_in_components==parcel_id]
                parcel_index = parcels.get_id_index(parcel_id)
                # what is already built on this parcel
                amount_built = parcels.get_attribute_by_index(unit_name, parcel_index)
                amount_proposed = to_be_built[pidx].sum()
                if amount_proposed > amount_built:
                    new_buildings["parcel_id"].append(parcel_id)
                    if unit_name == "residential_units":
                        bunit = "residential_units"
                        bnunit = "non_residential_sqft"
                    else:
                        bnunit = "residential_units"
                        bunit = "non_residential_sqft"
                    new_buildings[bunit].append(amount_built-amount_proposed)
                    new_buildings[bunit].append(0)
                    
            
        new_buildings["parcel_id"] = array(new_buildings["parcel_id"])
        new_buildings["residential_units"] = array(new_buildings["residential_units"])
        new_buildings["non_residential_sqft"] = array(new_buildings["non_residential_sqft"])
        new_buildings["building_id"] = max_building_id + arange(1, new_buildings["parcel_id"].size+1)
        new_buildings['year_built'] = resize(array([SimulationState().get_current_time()], dtype="int32"), 
                                             new_buildings["parcel_id"].size)
        building_dataset.add_elements(new_buildings, require_all_attributes=False)
        # remove active proposals from the proposal set
        development_proposal_set.remove_elements(active_idx)
        return development_proposal_set