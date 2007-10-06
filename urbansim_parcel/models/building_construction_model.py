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

from numpy import where, arange, resize, array, cumsum, concatenate, round_, any

class BuildingConstructionModel(Model):
    """Process any (pre-)scheduled development projects (those that have status 'active'). New buildings are 
    created according to the corresponding velocity function. The velocity function dataset is taken from dataset_pool.
    Buildings contained in the buildings_to_be_demolished list are removed from the building_set and any households
    and jobs placed in those buildings are unplaced.
    """
    model_name = "BuildingConstructionModel"

    def run (self, development_proposal_set, building_dataset, dataset_pool, buildings_to_be_demolished=[], 
             consider_amount_built_in_parcels = True, current_year=None):
        
        self.demolish_buildings(buildings_to_be_demolished, building_dataset, dataset_pool)

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
        
        if current_year is None:
            current_year = SimulationState().get_current_time()
            
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
        is_residential = building_type_set.get_attribute("is_residential")[index_in_building_types]==1
        unique_unit_names = unique_values(unit_names)
        
        # determine existing units on parcels
        parcels = dataset_pool.get_dataset("parcel")
        parcels.compute_variables(["urbansim_parcel.parcel.vacant_land_area"] + ["urbansim_parcel.parcel.residential_units"] + 
                                  map(lambda x: "urbansim_parcel.parcel.%s" % x, unique_unit_names), 
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
        parcel_vacant_land_area = parcels.get_attribute("vacant_land_area").astype(new_buildings["land_area"].dtype)
        number_of_new_buildings = {}
        
        # iterate over building types that are unique over the involved proposals
        for itype in range(unique_building_types.size):
            this_building_type = unique_building_types[itype]
            number_of_new_buildings[this_building_type] = 0
            unit_name = unit_names[itype]
            if is_residential[itype]:
                unit_name = 'residential_units'
            component_index = where(building_type_id == this_building_type)[0]
            parcel_ids_in_components = proposal_component_set.get_attribute_by_index("parcel_id", component_index)
            unique_parcels = unique_values(parcel_ids_in_components)
            # iterate over involved parcels
            for parcel_id in unique_parcels:
                pidx = component_index[parcel_ids_in_components==parcel_id]
                parcel_index = parcels.get_id_index(parcel_id)
                # what is already built on this parcel
                if consider_amount_built_in_parcels:
                    amount_built = parcels.get_attribute_by_index(unit_name, parcel_index)
                else:
                    amount_built = 0
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
                    to_be_built_cumsum = round_(cumsum(to_be_built[pidx])).astype("int32")
                    idx_to_be_built = where(to_be_built_cumsum > amount_built)[0]
                    new_buildings["parcel_id"] = concatenate((new_buildings["parcel_id"], 
                                                              array(idx_to_be_built.size * [parcel_id], dtype="int32")))
                    new_buildings[bunit] = concatenate((new_buildings[bunit], round_(to_be_built[pidx][idx_to_be_built]).astype(new_buildings[bunit].dtype)))
                    new_buildings[bnunit] = concatenate((new_buildings[bnunit], array(idx_to_be_built.size * [0], dtype="int32")))
                    new_buildings["building_type_id"] = concatenate((new_buildings["building_type_id"], 
                             array(idx_to_be_built.size * [this_building_type], dtype="int32")))
                    new_buildings["sqft_per_unit"] = concatenate((new_buildings["sqft_per_unit"],
                                                                  sqft_per_unit[pidx][idx_to_be_built]))
                    new_buildings["land_area"] = concatenate((new_buildings["land_area"], 
                                                              array(idx_to_be_built.size * [parcel_vacant_land_area[parcel_index]],
                                                                    dtype=new_buildings["land_area"].dtype)))
                    number_of_new_buildings[this_building_type] += idx_to_be_built.size
                    if parcel_is_lut_vacant[parcel_index]:
                        parcel_lut[parcel_index] = component_land_use_types[pidx][idx_to_be_built][0]
                                                                  
        # add created buildings to the existing building dataset
        buildings_id_name = building_dataset.get_id_name()[0]
        new_buildings[buildings_id_name] = max_building_id + arange(1, new_buildings["parcel_id"].size+1)
        new_buildings['year_built'] = resize(array([current_year], dtype="int32"), new_buildings["parcel_id"].size)
        building_dataset.add_elements(new_buildings, require_all_attributes=False)
        if "zone_id" in building_dataset.get_known_attribute_names():
            zone_ids = building_dataset.compute_variables(['building.disaggregate(parcel.zone_id)'], dataset_pool=dataset_pool)
            building_dataset.modify_attribute(name="zone_id", data=zone_ids)
        if "county" in building_dataset.get_known_attribute_names():
            county_ids = building_dataset.compute_variables(['building.disaggregate(parcel.county)'], dataset_pool=dataset_pool)
            building_dataset.modify_attribute(name="county", data=county_ids)
            
        logger.log_status("%s new buildings built." % new_buildings["parcel_id"].size)
        for type_id in number_of_new_buildings.keys():
            logger.log_status("building type %s: %s" % (type_id, number_of_new_buildings[type_id]))
            
        # remove active proposals from the proposal set
#        development_proposal_set.remove_elements(active_idx)
        # alternatively, set status_id of active proposals to id_not_available
        development_proposal_set.set_values_of_one_attribute("status_id", development_proposal_set.id_not_available, index=active_idx)
        dataset_pool._remove_dataset(proposal_component_set.get_dataset_name())
        return development_proposal_set
    
    def demolish_buildings(self, buildings_to_be_demolished, building_dataset, dataset_pool):
        if isinstance(buildings_to_be_demolished, list):
            buildings_to_be_demolished = array(buildings_to_be_demolished)
            
        if buildings_to_be_demolished.size <= 0:
            return
        
        building_dataset.remove_elements(building_dataset.get_id_index(buildings_to_be_demolished))
        logger.log_status("%s buildings demolished." % buildings_to_be_demolished.size)
        # remove occupants from demolished buildings
        buildings_id_name = building_dataset.get_id_name()[0]
        for agent_name in ['household', 'job']:            
            agents = dataset_pool.get_dataset(agent_name)
            location_ids = agents.get_attribute(buildings_id_name)
            id_index_in_buildings = building_dataset.try_get_id_index(location_ids)
            if any(id_index_in_buildings < 0):
                idx = where(id_index_in_buildings < 0)[0]
                agents.modify_attribute(name=buildings_id_name, data=idx.size*[-1], index = idx)
                logger.log_status("%s %ss removed from demolished buildings." % (idx.size, agent_name))
                
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import arange, array, all

class BuildingConstructionModelTest(opus_unittest.OpusTestCase):
    def test_demolition(self):
        household_data = {
            'household_id': arange(10)+1,
            'building_id': array([10, 3, 6, 150, 10, 10, -1, 5, 3, 3])
            }
        job_data = {
            'job_id': arange(5)+1,
            'building_id': array([180, 145, 10, 180, 179])
        }
        building_data = {
            'building_id': arange(200)+1,
            }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'households', table_data = household_data)
        storage.write_table(table_name = 'buildings', table_data = building_data)
        storage.write_table(table_name = 'jobs', table_data = job_data)
        dataset_pool = DatasetPool(storage = storage, package_order = ['urbansim_parcel', 'urbansim'])
        
        demolish_buildings = array([10, 3, 180])
        BCM = BuildingConstructionModel()
        BCM.demolish_buildings(demolish_buildings, dataset_pool.get_dataset('building'), dataset_pool)
        self.assertEqual(all(dataset_pool.get_dataset('household').get_attribute('building_id') ==
                                  array([-1, -1, 6, 150, -1, -1, -1, 5, -1, -1])), True)
        self.assertEqual(all(dataset_pool.get_dataset('job').get_attribute('building_id') ==
                                  array([-1, 145, -1, -1, 179])), True)
        self.assertEqual(dataset_pool.get_dataset('building').size()==197, True)
        
if __name__=="__main__":
    opus_unittest.main()