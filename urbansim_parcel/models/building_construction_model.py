# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model import Model
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from opus_core.logger import logger
from opus_core.misc import unique
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import DatasetSubset
from opus_core.join_attribute_modification_model import JoinAttributeModificationModel
from numpy import where, arange, resize, array, cumsum, concatenate, rint, any, logical_or, logical_and, logical_not

class BuildingConstructionModel(Model):
    """Process any (pre-)scheduled development projects (those that have status 'active'). New buildings are 
    created according to the corresponding velocity function. The velocity function dataset is taken from dataset_pool.
    Buildings contained in the buildings_to_be_demolished list are removed from the building_set and any households
    and jobs placed in those buildings are unplaced.
    """
    model_name = "BuildingConstructionModel"

    def run (self, development_proposal_set, building_dataset, dataset_pool, buildings_to_be_demolished=[], 
             consider_amount_built_in_parcels = False, current_year=None,
             development_proposal_component_set = None
             ):
        
        self.demolish_buildings(buildings_to_be_demolished, building_dataset, dataset_pool)

        if development_proposal_set.size() <= 0:
            logger.log_status("Proposal set is empty. Nothing to be constructed.")
            return development_proposal_set
        
        # load velocity function dataset
        try:
            velocity_function_set = dataset_pool.get_dataset("velocity_function")
        except:
            velocity_function_set = None
                
        # choose active projects
        is_active = development_proposal_set.get_attribute("status_id") == development_proposal_set.id_active
        is_delayed_or_active = logical_or(is_active, development_proposal_set.get_attribute("status_id") == development_proposal_set.id_with_velocity)
        active_idx = where(is_delayed_or_active)[0]
                                   
        if active_idx.size <= 0:
            logger.log_status("No new buildings built.")
            return development_proposal_set
        
        if current_year is None:
            current_year = SimulationState().get_current_time()
            
        # It is important that during this method no variable flushing happens, since
        # we create datasets of the same name  but different sizes than existing 
        # (possibly already flushed) datasets.
        flush_variables_current = SimulationState().get_flush_datasets()
        SimulationState().set_flush_datasets(False)
            
        active_proposal_set = DatasetSubset(development_proposal_set, active_idx)
        
        # create proposal_component_set from the active proposals
        if development_proposal_component_set is None:
            proposal_component_set = create_from_proposals_and_template_components(active_proposal_set, 
                                                   dataset_pool.get_dataset('development_template_component'))
        else:
            proposal_component_set = development_proposal_component_set
        dataset_pool.replace_dataset(proposal_component_set.get_dataset_name(), proposal_component_set)
        # determine building types and corresponding unit names of the involved building_types
        building_type_id = proposal_component_set.get_attribute("building_type_id")
        building_type_set = dataset_pool.get_dataset("building_type")
#        unit_names = building_type_set.compute_variables([
#                                  'building_type.disaggregate(generic_building_type.unit_name)'], dataset_pool=dataset_pool)
        unit_names = building_type_set.get_attribute("unit_name")
        # get unique values of the involved generic building types and unique unit names
        unique_building_types = unique(building_type_id)
        index_in_building_types = building_type_set.get_id_index(unique_building_types)
        unit_names = unit_names[index_in_building_types]
        is_residential = building_type_set.get_attribute("is_residential")[index_in_building_types]==1
        unique_unit_names = unique(unit_names)
        
        # determine existing units on parcels
        parcels = dataset_pool.get_dataset("parcel")
        parcels.compute_variables(["urbansim_parcel.parcel.vacant_land_area"] + ["urbansim_parcel.parcel.residential_units"] + 
                                  ["urbansim_parcel.parcel.%s" % x for x in unique_unit_names], 
                                  dataset_pool=dataset_pool)
        parcel_is_lut_vacant = parcels.compute_variables(["urbansim_parcel.parcel.is_land_use_type_vacant"], 
                                  dataset_pool=dataset_pool)
        parcel_lut = parcels.get_attribute("land_use_type_id")
        parcel_lut_before = parcel_lut.copy()
        if 'land_use_type_id' not in proposal_component_set.get_known_attribute_names():
            component_land_use_types = proposal_component_set.compute_variables([
              'development_project_proposal_component.disaggregate(development_template.land_use_type_id, [development_project_proposal])'],
                      dataset_pool=dataset_pool)
        else:
            component_land_use_types = proposal_component_set['land_use_type_id']
        component_is_redevelopment = proposal_component_set.compute_variables([
              'development_project_proposal_component.disaggregate(development_project_proposal.is_redevelopment)'],
                      dataset_pool=dataset_pool)
        

        # from the velocity function determine the amount to be built for each component (in %)
        if velocity_function_set is not None:
            cummulative_amount_of_development = proposal_component_set.compute_variables(["urbansim_parcel.development_project_proposal_component.cummulative_amount_of_development"], 
                                                                      dataset_pool=dataset_pool)
            percent_of_development_this_year = proposal_component_set.compute_variables(["urbansim_parcel.development_project_proposal_component.percent_of_development_this_year"], 
                                                                      dataset_pool=dataset_pool)
        else: # if there is no velocity function, all components have velocity of 100%
            percent_of_development_this_year = resize(array([100], dtype="int32"), int(proposal_component_set.size()))
                    
        # amount to be built
        to_be_built = proposal_component_set.compute_variables([
                    'urbansim_parcel.development_project_proposal_component.units_proposed'],
                                                 dataset_pool=dataset_pool)/100.0 * percent_of_development_this_year
        
        # initializing for new buildings
        max_building_id = building_dataset.get_id_attribute().max()
        new_buildings = {}
        new_buildings["parcel_id"] = array([], dtype="int32")
        new_buildings["residential_units"] = array([], dtype="int32")
        new_buildings["non_residential_sqft"] = array([], dtype="int32")
        new_buildings["building_type_id"] = array([], dtype="int32")
        new_buildings["sqft_per_unit"] = array([], dtype=building_dataset.get_attribute("sqft_per_unit").dtype)
        new_buildings["land_area"] = array([], dtype=building_dataset.get_attribute("land_area").dtype)
        new_buildings["improvement_value"] = array([], dtype=building_dataset.get_attribute("improvement_value").dtype)
        new_buildings["template_id"] = array([], dtype="int32")
        
        sqft_per_unit = proposal_component_set.get_attribute("building_sqft_per_unit").astype(new_buildings["sqft_per_unit"].dtype)
        # Compute land_area_taken properly if velocity function is present
        if velocity_function_set is not None:
            larea_taken = proposal_component_set.compute_variables(['urbansim_parcel.development_project_proposal_component.land_area_taken'],
                                                                   dataset_pool=dataset_pool)
            pct_dev_this_yr_conv = (percent_of_development_this_year / 100.0)
            land_area_taken = larea_taken * pct_dev_this_yr_conv
        else:
            land_area_taken = proposal_component_set.compute_variables(['urbansim_parcel.development_project_proposal_component.land_area_taken'],
                                                                   dataset_pool=dataset_pool).astype(new_buildings["land_area"].dtype)
        construction_cost = proposal_component_set.compute_variables(['urbansim_parcel.development_project_proposal_component.construction_cost'],
                                                                   dataset_pool=dataset_pool).astype(new_buildings["improvement_value"].dtype)
        template_ids = proposal_component_set.get_attribute("template_id")
        number_of_new_buildings = {}
        number_of_new_buildings_by_template_id = {}
        
        # iterate over building types that are unique over the involved proposals
        for itype in range(unique_building_types.size):
            this_building_type = unique_building_types[itype]
            number_of_new_buildings[this_building_type] = 0
            unit_name = unit_names[itype]
            if is_residential[itype]:
                unit_name = 'residential_units'
            component_index = where(building_type_id == this_building_type)[0]
            parcel_ids_in_components = proposal_component_set.get_attribute_by_index("parcel_id", component_index)
            unique_parcels = unique(parcel_ids_in_components)
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
                if rint(amount_proposed) > amount_built:
                    if unit_name == "residential_units":
                        bunit = "residential_units"
                        bnunit = "non_residential_sqft"
                    else:
                        bnunit = "residential_units"
                        bunit = "non_residential_sqft"
                    to_be_built_cumsum = rint(cumsum(to_be_built[pidx])).astype("int32")
                    idx_to_be_built = where(to_be_built_cumsum > amount_built)[0]
                    new_buildings["parcel_id"] = concatenate((new_buildings["parcel_id"], 
                                                              array(idx_to_be_built.size * [parcel_id], dtype="int32")))
                    new_buildings[bunit] = concatenate((new_buildings[bunit], rint(to_be_built[pidx][idx_to_be_built]).astype(new_buildings[bunit].dtype)))
                    new_buildings[bnunit] = concatenate((new_buildings[bnunit], array(idx_to_be_built.size * [0], dtype="int32")))
                    new_buildings["building_type_id"] = concatenate((new_buildings["building_type_id"], 
                             array(idx_to_be_built.size * [this_building_type], dtype="int32")))
                    new_buildings["sqft_per_unit"] = concatenate((new_buildings["sqft_per_unit"],
                                                                  sqft_per_unit[pidx][idx_to_be_built]))
                    new_buildings["land_area"] = concatenate((new_buildings["land_area"], land_area_taken[pidx][idx_to_be_built]))
                    new_buildings["improvement_value"] = concatenate((new_buildings["improvement_value"], construction_cost[pidx][idx_to_be_built]))
                    new_buildings["template_id"] = concatenate((new_buildings["template_id"], template_ids[pidx][idx_to_be_built]))
                    number_of_new_buildings[this_building_type] += idx_to_be_built.size
                    if parcel_is_lut_vacant[parcel_index] or component_is_redevelopment[pidx][idx_to_be_built][0]:
                        parcel_lut[parcel_index] = component_land_use_types[pidx][idx_to_be_built][0]
                    # count number of buildings by template ids
                    for icomp in range(idx_to_be_built.size):
                        if template_ids[pidx[idx_to_be_built[icomp]]] not in list(number_of_new_buildings_by_template_id.keys()):
                            number_of_new_buildings_by_template_id[template_ids[pidx[idx_to_be_built[icomp]]]] = 0
                        number_of_new_buildings_by_template_id[template_ids[pidx[idx_to_be_built[icomp]]]] += 1
                                                                  
        # add created buildings to the existing building dataset
        buildings_id_name = building_dataset.get_id_name()[0]
        new_buildings[buildings_id_name] = max_building_id + arange(1, new_buildings["parcel_id"].size+1)
        new_buildings['year_built'] = resize(array([current_year], dtype="int32"), new_buildings["parcel_id"].size)
        new_buildings['job_capacity'] = resize(array([-1], dtype="int32"), new_buildings["parcel_id"].size)
        building_dataset.add_elements(new_buildings, require_all_attributes=False)
        if "zone_id" in building_dataset.get_known_attribute_names():
            zone_ids = building_dataset.compute_variables(['building.disaggregate(parcel.zone_id)'], dataset_pool=dataset_pool)
            building_dataset.modify_attribute(name="zone_id", data=zone_ids)
        if "county" in building_dataset.get_known_attribute_names():
            county_ids = building_dataset.compute_variables(['building.disaggregate(parcel.county)'], dataset_pool=dataset_pool)
            building_dataset.modify_attribute(name="county", data=county_ids)
            
        logger.log_status("%s new buildings built." % new_buildings["parcel_id"].size)
        for type_id in list(number_of_new_buildings.keys()):
            logger.log_status("building type %s: %s" % (type_id, number_of_new_buildings[type_id]))
        logger.log_status("Number of new buildings by template ids:")
        logger.log_status(number_of_new_buildings_by_template_id)
        parcels["land_use_type_id"] = parcel_lut
        logger.log_status("%s parcels have modified land_use_type_id." % (parcel_lut_before != parcel_lut).sum())
        
        # recompute the cummulative development amount
        if velocity_function_set is not None:
            # determine, if everything has been built or if it should be considered next year
            cummulative_amount_of_development = development_proposal_set.compute_variables([
              "development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.cummulative_amount_of_development)/urbansim_parcel.development_project_proposal.number_of_components"], 
                                                                      dataset_pool=dataset_pool)
        else: # if there is no velocity function, all components have velocity of 100%
            ## TODO: need to be reviewed, probably by Hana
            ## changed from proposal_component_set to development_proposal_set
            ## so it will have the same shape as is_delayed_or_active
            cummulative_amount_of_development = resize(array([100], dtype="int32"), int(development_proposal_set.size()))
        will_be_delayed = cummulative_amount_of_development < 100
        velocity_idx = where(logical_and(is_delayed_or_active, will_be_delayed))[0]
        if velocity_idx.size > 0:
            # for the unfinished projects set the status_id to id_with_velocity 
            development_proposal_set.set_values_of_one_attribute("status_id", development_proposal_set.id_with_velocity, index=velocity_idx)
        not_velocity_idx = where(logical_and(is_delayed_or_active, logical_not(will_be_delayed)))[0]
        if not_velocity_idx.size > 0:
            # for the remaining projects set the status_id to id_not_available
            development_proposal_set.set_values_of_one_attribute("status_id", development_proposal_set.id_not_available, index=not_velocity_idx)
            
        dataset_pool._remove_dataset(proposal_component_set.get_dataset_name())
        # switch flush_variables to the original value
        SimulationState().set_flush_datasets(flush_variables_current)
        return development_proposal_set
    
    def demolish_buildings(self, buildings_to_be_demolished, building_dataset, dataset_pool):
        if isinstance(buildings_to_be_demolished, list):
            buildings_to_be_demolished = array(buildings_to_be_demolished)
            
        if buildings_to_be_demolished.size <= 0:
            return
        
        id_index_in_buildings = building_dataset.get_id_index(buildings_to_be_demolished)
        parcels = dataset_pool.get_dataset('parcel')
        idx_pcl = parcels.get_id_index(unique(building_dataset['parcel_id'][id_index_in_buildings]))
        # remove occupants from buildings to be demolished
        JAMM = JoinAttributeModificationModel()
        for agent_name in ['household', 'job']:            
            agents = dataset_pool.get_dataset(agent_name)
            JAMM.run(agents, building_dataset, index=id_index_in_buildings, value=-1)
            
        building_dataset.remove_elements(id_index_in_buildings)
        logger.log_status("%s buildings demolished." % buildings_to_be_demolished.size)
        
        # set land_use_type 'vacant' to parcels with demolished buildings
        land_types = dataset_pool.get_dataset('land_use_type')
        vac_idx = land_types["land_use_name"] == 'vacant'
        if vac_idx.sum() > 0:
            code = land_types.get_id_attribute()[vac_idx][0]
            nvac = (parcels['land_use_type_id'][idx_pcl] == code).sum()
            parcels['land_use_type_id'][idx_pcl] = code
            logger.log_status("%s parcels set to vacant." % (idx_pcl.size - nvac))

                
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import arange, array, all


class BuildingConstructionModelTest(opus_unittest.OpusTestCase):
    def test_demolition(self):
        demolish_buildings = array([10, 3, 180])
        household_data = {
            'household_id': arange(10)+1,
            'building_id': array([10, 3, 6, 150, 10, 10, -1, 5, 3, 3])
            # demolished         [*   *           *   *         *  *]
            }
        person_data = {
            'person_id':arange(15)+1,
            'household_id': array([1,1,2,3,3,5,4,4,4,6,7,8,9,10,10]),
           # in demolished bldgs  [* * *     *       * *   *  *  *]
            'job_id':       array([5,4,1,2,2,1,3,5,1,5,5,4,3, 3, 1])
           # in demolished bldgs  [  * *     * *   *     * *  *  *]
                       }
        job_data = {
            'job_id': arange(5)+1,
            'building_id': array([180, 145, 10, 180, 179])
        }
        building_data = {
            'building_id': arange(200)+1,
            'parcel_id': arange(200)+1
            }        
        parcel_data = {
            'parcel_id': arange(200)+1,
            'land_use_type_id': array(150*[1]+50*[2]),      
            }
        
        lut_data = {
            'land_use_type_id': array([1,2]),
            'land_use_name': array(['non_vacant', 'vacant'])        
            }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'households', table_data = household_data)
        storage.write_table(table_name = 'buildings', table_data = building_data)
        storage.write_table(table_name = 'jobs', table_data = job_data)
        storage.write_table(table_name = 'persons', table_data = person_data)
        storage.write_table(table_name = 'parcels', table_data = parcel_data)
        storage.write_table(table_name = 'land_use_types', table_data = lut_data)
        dataset_pool = DatasetPool(storage = storage, package_order = ['urbansim_parcel', 'urbansim'])
        
        
        BCM = BuildingConstructionModel()
        BCM.demolish_buildings(demolish_buildings, dataset_pool.get_dataset('building'), dataset_pool)
        JAMM = JoinAttributeModificationModel()
        JAMM.run(dataset_pool.get_dataset('person'), dataset_pool.get_dataset('household'), 
                 attribute_to_be_modified='job_id', value=-1, filter='household.building_id <=0')
        JAMM.run(dataset_pool.get_dataset('person'), dataset_pool.get_dataset('job'), 
                 attribute_to_be_modified='job_id', value=-1, filter='job.building_id <=0')
        self.assertEqual(all(dataset_pool.get_dataset('household').get_attribute('building_id') ==
                                  array([-1, -1, 6, 150, -1, -1, -1, 5, -1, -1])), True)
        self.assertEqual(all(dataset_pool.get_dataset('job').get_attribute('building_id') ==
                                  array([-1, 145, -1, -1, 179])), True)
        self.assertEqual(dataset_pool.get_dataset('building').size()==197, True)
        self.assertEqual(all(dataset_pool.get_dataset('person').get_attribute('job_id') == 
                             array([-1,-1,-1,2,2,-1,-1,5,-1,-1,-1,-1,-1,-1,-1])), True)
        self.assertEqual(dataset_pool.get_dataset('parcel')['land_use_type_id'][9], 2)
        self.assertEqual(dataset_pool.get_dataset('parcel')['land_use_type_id'][2], 2)            
        
if __name__=="__main__":
    opus_unittest.main()