# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.sampling_toolbox import sample_noreplace, probsample_noreplace
from opus_core.datasets.dataset import Dataset, DatasetSubset
from opus_core.misc import unique_values
from opus_core.variables.variable_name import VariableName
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from numpy import zeros, arange, where, ones, logical_or, logical_and, logical_not, int32, float32, sometrue
from numpy import compress, take, alltrue, argsort, array, int8, bool8, ceil, sort, minimum, concatenate
from gc import collect
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from opus_core.model import Model
from scipy import ndimage

class DevelopmentProjectProposalSamplingModel(Model):

    def __init__(self, proposal_set,
                 sampler="opus_core.samplers.weighted_sampler",
                 weight_string = "exp_roi = exp(urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment)",
                 filter_attribute=None,
                 run_config=None, estimate_config=None,
                 debuglevel=0, dataset_pool=None):
        """
        this model sample project proposals from proposal set weighted by exponentiated ROI
        """
        self.dataset_pool = self.create_dataset_pool(dataset_pool, pool_packages=['urbansim_parcel', 'urbansim', 'opus_core'])
        self.dataset_pool.add_datasets_if_not_included({proposal_set.get_dataset_name(): proposal_set})
        self.proposal_set = proposal_set
        if not self.dataset_pool.has_dataset("development_project_proposal_component"):
            self.proposal_component_set = create_from_proposals_and_template_components(proposal_set, 
                                                       self.dataset_pool.get_dataset('development_template_component'))
            self.dataset_pool.replace_dataset(self.proposal_component_set.get_dataset_name(), self.proposal_component_set)
        else:
            self.proposal_component_set = self.dataset_pool.get_dataset("development_project_proposal_component")

        if weight_string is not None:
            if weight_string not in proposal_set.get_known_attribute_names():
                proposal_set.compute_variables(weight_string, dataset_pool=self.dataset_pool)
            self.weight = self.proposal_set.get_attribute(weight_string)
        else:
            self.weight = ones(self.proposal_set.size(), dtype="float64")  #equal weight

        ## TODO: handling of filter_attribute
#        if filter_attribute is not None:
#            if filter_attribute not in proposal_set.get_known_attribute_names():
#                proposal_set.compute_variables(filter_attribute)
#            elif not isinstance(filter_attribute, array):
#
#            self.weight = self.weight * proposal_set.get_attribute(filter_attribute)


    def run(self, n=500, run_config=None, current_year=None, debuglevel=0):
        """
        n - sample n proposals at a time, evaluate them one by one
        """
        if current_year is None:
            current_year = SimulationState().get_current_time()

        self.proposal_component_set.compute_variables([
            'urbansim_parcel.development_project_proposal_component.units_proposed',
            'urbansim_parcel.development_project_proposal_component.is_residential'],
                                        dataset_pool=self.dataset_pool)
        self.proposal_set.compute_variables([
            'urbansim_parcel.development_project_proposal.number_of_components',
            'zone_id=development_project_proposal.disaggregate(parcel.zone_id)',
            #'occurence_frequency = development_project_proposal.disaggregate(development_template.sample_size)'
            ],
                                        dataset_pool=self.dataset_pool)
        buildings = self.dataset_pool.get_dataset("building")
        buildings.compute_variables([
                                "occupied_units_for_jobs = urbansim_parcel.building.number_of_non_home_based_jobs",
                                "units_for_jobs = urbansim_parcel.building.total_non_home_based_job_space",
                                "occupied_residential_units = urbansim_parcel.building.number_of_households",
#                                "urbansim_parcel.building.existing_units",
                                "urbansim_parcel.building.is_residential"
                                    ],
                                    dataset_pool=self.dataset_pool)
        parcels = self.dataset_pool.get_dataset('parcel')
        parcels.compute_variables(['urbansim_parcel.parcel.building_sqft', 'urbansim_parcel.parcel.residential_units'],
                                  dataset_pool=self.dataset_pool)

        ## define unit_name by whether a building is residential or not (with is_residential attribute)
        ## if it is non-residential (0), count units by number of job spaces (units_for_jobs)
        ## if it is residential (1), count units by residenital units
        self.unit_name = array(["units_for_jobs", "residential_units"])
                
        target_vacancy = self.dataset_pool.get_dataset('target_vacancy')
        target_vacancy.compute_variables(['is_residential = target_vacancy.disaggregate(building_type.is_residential)'],
                                         dataset_pool=self.dataset_pool)
        current_target_vacancy = DatasetSubset(target_vacancy, index=where(target_vacancy.get_attribute("year")==current_year)[0])

        self.existing_units = {}   #total existing units by land_use type
        self.occupied_units = {}   #total occupied units by land_use type
        self.proposed_units = {}   #total proposed units by land_use type
        self.demolished_units = {} #total (to be) demolished units by land_use type
        self.demolished_buildings = array([], dtype='int32')  #id of buildings to be demolished

        components_building_type_ids = self.proposal_component_set.get_attribute("building_type_id").astype("int32")
        proposal_ids = self.proposal_set.get_id_attribute()
        proposal_ids_in_component_set = self.proposal_component_set.get_attribute("proposal_id")
        all_units_proposed = self.proposal_component_set.get_attribute("units_proposed")
        number_of_components_in_proposals = self.proposal_set.get_attribute("number_of_components")
        
        self.accepting_proposals = zeros(current_target_vacancy.get_attribute("building_type_id").max()+1, dtype='bool8')  #whether accepting new proposals, for each building type
        self.accepted_proposals = [] # index of accepted proposals

        self.target_vacancies = {}
        tv_building_types = current_target_vacancy.get_attribute("building_type_id")
        tv_rate = current_target_vacancy.get_attribute("target_vacancy_rate")
        for itype in range(tv_building_types.size):
            self.target_vacancies[tv_building_types[itype]] = tv_rate[itype]
            
        self.check_vacancy_rates(current_target_vacancy)  #initialize self.accepting_proposal based on current vacancy rate

        sqft_per_job = self.dataset_pool.get_dataset("building_sqft_per_job")
        zones_of_proposals = self.proposal_set.get_attribute("zone_id")
        self.building_sqft_per_job_table = sqft_per_job.get_building_sqft_as_table(zones_of_proposals.max(), 
                                                                                   tv_building_types.max())
        # consider only those proposals that have all components of accepted type and sum of proposed units > 0
        is_accepted_type = self.accepting_proposals[components_building_type_ids]
        sum_is_accepted_type_over_proposals = array(ndimage.sum(is_accepted_type, labels = proposal_ids_in_component_set, 
                                                          index = proposal_ids))
        sum_of_units_proposed = array(ndimage.sum(all_units_proposed, labels = proposal_ids_in_component_set, 
                                                          index = proposal_ids))
        is_proposal_eligible = logical_and(sum_is_accepted_type_over_proposals == number_of_components_in_proposals,
                                           sum_of_units_proposed > 0)

        is_proposal_eligible = logical_and(is_proposal_eligible,
                                           self.proposal_set.get_attribute("start_year")==current_year )
        ## handle planned proposals: all proposals with status_id == is_planned 
        ## and start_year == current_year are accepted
        planned_proposal_indexes = where(logical_and(
                                                  self.proposal_set.get_attribute("status_id") == self.proposal_set.id_planned, 
                                                  self.proposal_set.get_attribute("start_year") == current_year ) 
                                        )[0] 
                                   
        self.consider_proposals(planned_proposal_indexes, force_accepting=True)
        # consider proposals (in this order: planned, proposed, tentative)
        for status in [self.proposal_set.id_proposed, self.proposal_set.id_tentative]:
            idx = where(logical_and(self.proposal_set.get_attribute("status_id") == status, is_proposal_eligible))[0]
            if idx.size <= 0:
                continue
            logger.log_status("Sampling from %s eligible proposals with status %s." % (idx.size, status))
            while (True in self.accepting_proposals):
                if self.weight[idx].sum() == 0.0:
                    logger.log_warning("Running out of proposals; there aren't any proposals with non-zero weight")
                    break
                
                idx = idx[self.weight[idx] > 0]
                n = minimum(idx.size, n)
                sampled_proposal_indexes = probsample_noreplace(proposal_ids[idx], n, 
                                                prob_array=(self.weight[idx]/float(self.weight[idx].sum())),                                                                
                                                exclude_index=None, return_indices=True)
                self.consider_proposals(arange(self.proposal_set.size())[idx[sampled_proposal_indexes]])
                self.weight[idx[sampled_proposal_indexes]] = 0

        # set status of accepted proposals to 'active'
        self.proposal_set.modify_attribute(name="status_id", data=self.proposal_set.id_active,
                                          index=array(self.accepted_proposals, dtype='int32'))
        building_types = self.dataset_pool.get_dataset("building_type")
        logger.log_status("Status of %s development proposals set to active." % len(self.accepted_proposals))
        logger.log_status("Target/existing vacancy rates (reached using eligible proposals) by building type:")
        for type_id in self.existing_units.keys():
            units_stock = self._get_units_stock(type_id)
            vr = self._get_vacancy_rates(type_id)
            ## units = residential_units if building_type is residential
            ## units = number of job spaces if building_type is non-residential
            logger.log_status(
                              """%(type_id)s[%(type_name)s]: %(vr)s = ((existing_units:%(existing_units)s + 
                              units_proposed:%(units_proposed)s - units_to_be_demolished:%(units_demolished)s) 
                              - units_occupied:%(units_occupied)s) / units_stock:%(units_stock)s""" %  \
                                          { 'type_id': type_id,
                                            'type_name': building_types.get_attribute_by_id("building_type_name", type_id),
                                            'vr':  vr,
                                            'existing_units': int(self.existing_units[type_id]),
                                            'units_occupied': int(self.occupied_units[type_id]),
                                            'units_proposed': int(self.proposed_units[type_id]),
                                            'units_demolished': int(self.demolished_units[type_id]),
                                            'units_stock': int(units_stock)
                                          }
                            )
        
        return (self.proposal_set, self.demolished_buildings) 

    def check_vacancy_rates(self, target_vacancy):
        type_ids = target_vacancy.get_attribute("building_type_id")
        is_residential = target_vacancy.get_attribute("is_residential")
        buildings = self.dataset_pool.get_dataset("building")
        building_type_ids = buildings.get_attribute("building_type_id")
        for index in arange(target_vacancy.size()):
            type_id = type_ids[index]
            target = self.target_vacancies[type_id]           
            is_matched_type = building_type_ids == type_id
                
            self.existing_units[type_id] = buildings.get_attribute(self.unit_name[is_residential[index]])[is_matched_type].astype("float32").sum()
            self.occupied_units[type_id] = buildings.get_attribute("occupied_%s" % self.unit_name[is_residential[index]])[is_matched_type].astype("float32").sum()          
            self.proposed_units[type_id] = 0
            self.demolished_units[type_id] = 0
            vr = self._get_vacancy_rates(type_id)
            
            if vr < target:
                self.accepting_proposals[type_id] = True

    def consider_proposals(self, proposal_indexes, force_accepting=False):

        proposals_parcel_ids = self.proposal_set.get_attribute("parcel_id")
        
        components_building_type_ids = self.proposal_component_set.get_attribute("building_type_id").astype("int32")
        proposal_ids = self.proposal_set.get_id_attribute()
        proposal_ids_in_component_set = self.proposal_component_set.get_attribute("proposal_id")
        all_units_proposed = self.proposal_component_set.get_attribute("units_proposed")
        is_component_residential = self.proposal_component_set.get_attribute("is_residential")
        number_of_components_in_proposals = self.proposal_set.get_attribute("number_of_components")
        zones_of_proposals = self.proposal_set.get_attribute("zone_id")
        is_proposal_rejected = zeros(proposal_indexes.size, dtype=bool8)
        proposal_site = proposals_parcel_ids[proposal_indexes]
        is_redevelopment = self.proposal_set.get_attribute_by_index("is_redevelopment", proposal_indexes)
        buildings = self.dataset_pool.get_dataset("building")
        building_site = buildings.get_attribute("parcel_id")
#        building_existing_units = buildings.get_attribute("existing_units")
        is_residential = buildings.get_attribute("is_residential")
        building_type_ids = buildings.get_attribute("building_type_id")
        building_ids = buildings.get_id_attribute()
        
        for i in range(proposal_indexes.size):
            if not (True in self.accepting_proposals):
                # if none of the types is accepting_proposals, exit
                # this is put in the loop to check if the last accepted proposal has sufficed
                # the target vacancy rates for all types
                return
            if is_proposal_rejected[i]:
                continue
            proposal_index = proposal_indexes[i]  # consider 1 proposed project at a time
            proposal_index_in_component_set = where(proposal_ids_in_component_set == proposal_ids[proposal_index])[0]
            units_proposed = all_units_proposed[proposal_index_in_component_set]
            component_types = components_building_type_ids[proposal_index_in_component_set]
            is_this_component_residential = is_component_residential[proposal_index_in_component_set]
            this_site = proposal_site[i]
            
            if is_redevelopment[i]:  #redevelopment proposal           
                affected_building_index = where(building_site==this_site)[0]
                for this_building in affected_building_index:
                    this_building_type = building_type_ids[this_building]
                    if this_building_type in self.existing_units.keys():
                        _unit_name = self.unit_name[is_residential[this_building]]
                        self.demolished_units[this_building_type] += buildings.get_attribute(_unit_name)[this_building]    #demolish affected buildings
                                                
                    self.demolished_buildings = concatenate( (self.demolished_buildings,  array([building_ids[this_building]] )))
#                self.occupied_units[type_id] = buildings.get_attribute("occupied_%s" % unit_name)[is_matched_type].astype("float32").sum()          
                
            for itype_id in range(component_types.size): #
                # this loop is only needed when a proposal could provide units of more than 1 generic building types
                type_id = component_types[itype_id]
   
                if is_this_component_residential[itype_id]:
                    self.proposed_units[type_id] += units_proposed[itype_id]
                else: # translate from building_sqft to number of job spaces
                    self.proposed_units[type_id] += units_proposed[itype_id] / \
                                                    self.building_sqft_per_job_table[zones_of_proposals[proposal_indexes[i]], type_id]
                if not force_accepting:                                
                    ## consider whether target vacancy rates have been achieved if not force_accepting
                    units_stock = self._get_units_stock(type_id)
                    vr = self._get_vacancy_rates(type_id)
                    if vr >= self.target_vacancies[type_id]:
                        ## not accepting proposals of this type
                        self.accepting_proposals[type_id] = False
                        ## reject all proposals to be processed that have one of the components of this type
                        consider_idx = proposal_indexes[(i+1):proposal_indexes.size]
                        if consider_idx.size > 0:
                            is_accepted_type = self.accepting_proposals[components_building_type_ids]
                            sum_is_accepted_type_over_proposals = array(ndimage.sum(is_accepted_type, 
                                                                                labels = proposal_ids_in_component_set, 
                                                              index = proposal_ids[consider_idx]))                   
                            is_rejected_indices = where(sum_is_accepted_type_over_proposals < 
                                                    number_of_components_in_proposals[consider_idx])[0]
                            is_proposal_rejected[arange((i+1),proposal_indexes.size)[is_rejected_indices]] = True
                            self.weight[consider_idx[is_rejected_indices]] = 0.0

            if not is_proposal_rejected[i]:
                # proposal accepted
                self.accepted_proposals.append(proposal_index)
            # reject all pending proposals for this site (1 site can accept only 1 proposal at any 1 given year)
            is_proposal_rejected[proposal_site == this_site] = True
            # don't consider proposals for this site in future sampling (in this year's developer model)
            self.weight[proposals_parcel_ids == this_site] = 0.0
            # if all proposals in proposal_indexes have being rejected, return 
            if is_proposal_rejected.sum() == is_proposal_rejected.size:
                return
            
    def _get_units_stock(self, type_id):
        units_stock = self.existing_units[type_id] - self.demolished_units[type_id] + self.proposed_units[type_id]
        return units_stock

    def _get_vacancy_rates(self, type_id):
        units_stock = self._get_units_stock(type_id)
        vacant_units =  units_stock - self.occupied_units[type_id]
        if vacant_units < 0:  
        #vacant units should be no less than 0, so that the minimum vacancy rate is 0
            vacant_units = 0
        vr = vacant_units/float(units_stock)
        return vr  

from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import arange, array, all
from opus_core.datasets.dataset import Dataset

class DevelopmentProjectProposalSamplingModelTest(opus_unittest.OpusTestCase):
    def test_vacancy_rates_calculation(self):

        proposal_data = {
            'proposal_id': array([1]),
            }
        proposal_component_data = {
            'component_id':array([1]),
            }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'development_project_proposals', table_data = proposal_data)
        storage.write_table(table_name = 'development_project_proposal_components', table_data = proposal_component_data)
        dataset_pool = DatasetPool(storage = storage, package_order = ['urbansim_parcel', 'urbansim'])
                       
        proposal_dataset = dataset_pool.get_dataset('development_project_proposal')
        proposal_component_dataset = dataset_pool.get_dataset('development_project_proposal_component')
 
        DPPSM = DevelopmentProjectProposalSamplingModel(proposal_dataset, dataset_pool=dataset_pool, weight_string=None)
        DPPSM.existing_units =   {1:200, 2:200, 3:200, 4:200, 5:200, 6:200}
        DPPSM.demolished_units = {1:100, 2:100, 3:100, 4:50,  5:0,   6:20}
        DPPSM.proposed_units =   {1:50,  2:150, 3:80,  4:100, 5:160, 6:0}
        DPPSM.occupied_units =   {1:180, 2:180, 3:180, 4:180, 5:180, 6:180}
        
        expected = {1:0.0, 2:0.28, 3:0.0, 4:0.28, 5:0.5, 6:0.0}
        actual = {}
        for type in DPPSM.existing_units.keys():
            actual[type] = DPPSM._get_vacancy_rates(type)

        self.assertDictsEqual(actual, expected)
        
if __name__=="__main__":
    opus_unittest.main()
