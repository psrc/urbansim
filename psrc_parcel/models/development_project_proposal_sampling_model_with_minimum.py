# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim_parcel.models.development_project_proposal_sampling_model2 import DevelopmentProjectProposalSamplingModel as USDevelopmentProjectProposalSamplingModel
from opus_core.resources import Resources
from opus_core.sampling_toolbox import sample_noreplace, probsample_noreplace
from opus_core.datasets.dataset import Dataset, DatasetSubset
from opus_core.variables.variable_name import VariableName
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from numpy import zeros, arange, where, ones, logical_or, logical_and, logical_not, int32, float32, sometrue, setdiff1d, union1d
from numpy import compress, take, alltrue, argsort, array, int8, bool8, ceil, sort, minimum, concatenate, in1d, argsort, log, exp
from scipy.ndimage import minimum as ndimage_min
from scipy.ndimage import maximum as ndimage_max
from scipy.ndimage import mean as ndimage_mean
from scipy.ndimage import maximum_position
from gc import collect
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from opus_core.model import Model
from opus_core import ndimage
from opus_core.misc import unique, ismember, intersect1d
from collections import defaultdict

class DevelopmentProjectProposalSamplingModel(USDevelopmentProjectProposalSamplingModel):
    """The model takes into account an additional column of the target vacancy table (called "minimum_spaces" by default).
    It stops building if both conditions are true: enough space as defined by vacancy rate, 
    AND at least "minimum_spaces" units were built.
    It also implements the sampling in two phases:
    1. Selecting one proposal within each parcel and building type, in order not to give too much advantage to parcels with a large amount of proposals. 
    2. Between parcel sampling - the same as the parent model.
    """
    
    def __init__(self, proposal_set,
                 weight_string = "exp_roi=exp(urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment)",
                 filter_attribute=None, **kwargs):
        USDevelopmentProjectProposalSamplingModel.__init__(self, proposal_set, weight_string=weight_string, 
                                                           filter_attribute=None, **kwargs)
        self.proposal_set.id_eliminated_in_within_parcel_selection = 44
        self.proposal_set.id_no_demand = 43
        self.proposal_set.id_weights_zero = 41
        self.proposal_set.id_filter_not_passed = 42
        self.proposal_set['status_id'][where((self.weight == 0)*(self.proposal_set['status_id'] == self.proposal_set.id_tentative))] = self.proposal_set.id_weights_zero   

        if filter_attribute is not None:
            if VariableName(filter_attribute).get_alias() not in self.proposal_set.get_known_attribute_names():
                self.proposal_set.compute_variables(filter_attribute)
            where_not_passed = where((self.proposal_set[filter_attribute]==0)*(self.proposal_set['status_id'] == self.proposal_set.id_tentative))[0]
            if where_not_passed.size > 0:
                self.proposal_set['status_id'][where_not_passed] = self.proposal_set.id_filter_not_passed
                logger.log_status("%s proposals did not pass given filter and were eliminated." % where_not_passed.size)
            self.weight = self.weight * (self.proposal_set.get_attribute(filter_attribute) >=1)

    
    def run(self, n=500, 
            realestate_dataset_name = 'building',
            current_year=None,
            occupied_spaces_variable="occupied_spaces",
            total_spaces_variable="total_spaces",
            minimum_spaces_attribute="minimum_spaces",
            within_parcel_selection_weight_string=None,
            within_parcel_selection_n=0,
            within_parcel_selection_compete_among_types=False,
            within_parcel_selection_threshold=75,
            within_parcel_selection_MU_same_weight=False,
            within_parcel_selection_transpose_interpcl_weight=True,
            run_config=None,
            debuglevel=0):
        """
        run method of the Development Project Proposal Sampling Model
        
        **Parameters**
        
            **n** : int, sample size for each iteration
                   
                   sample n proposals at a time, which are then evaluated one by one until the 
                   target vacancies are satisfied or proposals are running out
                   
            **realestate_dataset_name** : string, name of real estate dataset
            
            **current_year**: int, simulation year. If None, get value from SimulationState
            
            **occupied_spaces_variable** : string, variable name for calculating how much spaces are currently occupied
                                        
                                          It can either be a variable for real_estate dataset that returns 
                                          the amount spaces being occupied or a target_vacancy attribute 
                                          that contains the name of real_estate variables.   
            
            **total_spaces_variable** : string, variable name for calculating total existing spaces
            
        **Returns**
        
            **proposal_set** : indices to proposal_set that are accepted 
            
            **demolished_buildings** : buildings to be demolished for re-development
        """

        self.accepted_proposals = []
        self.demolished_buildings = []  #id of buildings to be demolished

        if self.proposal_set.n <= 0:
            logger.log_status("The size of proposal_set is 0; no proposals to consider, skipping DPPSM.")
            return (self.proposal_set, self.demolished_buildings)

        target_vacancy = self.dataset_pool.get_dataset('target_vacancy')

        if current_year is None:
            year = SimulationState().get_current_time()
        else:
            year = current_year
        this_year_index = where(target_vacancy['year']==year)[0]
        target_vacancy_for_this_year = DatasetSubset(target_vacancy, this_year_index)
        if target_vacancy_for_this_year.size() == 0:
            raise IOError, 'No target vacancy defined for year %s.' % year
        
        ## current_target_vacancy.target_attribute_name = 'target_vacancy_rate'
        ## each column provides a category for which a target vacancy is specified
        self.column_names = list(set( target_vacancy.get_known_attribute_names() ) - \
                            set( [ target_vacancy.target_attribute_name, 
                                   'year', '_hidden_id_', minimum_spaces_attribute,
                                   occupied_spaces_variable, total_spaces_variable
                                   ] )
                            )
        self.column_names.sort(reverse=True)
            
        ## buildings table provides existing stocks
        self.realestate_dataset = self.dataset_pool.get_dataset(realestate_dataset_name)
        
        occupied_spaces_variables = [occupied_spaces_variable]
        total_spaces_variables = [total_spaces_variable]
        if occupied_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
            occupied_spaces_variables += unique(target_vacancy_for_this_year[occupied_spaces_variable]).tolist()
        if total_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
            total_spaces_variables += unique(target_vacancy_for_this_year[total_spaces_variable]).tolist()
            
        self._compute_variables_for_dataset_if_needed(self.realestate_dataset, self.column_names + occupied_spaces_variables + total_spaces_variables)
        self._compute_variables_for_dataset_if_needed(self.proposal_component_set, self.column_names + total_spaces_variables)
        self.proposal_set.compute_variables(["urbansim_parcel.development_project_proposal.number_of_components", 
                                             "urbansim_parcel.development_project_proposal.land_area_taken"],
                                            dataset_pool=self.dataset_pool)
        
        n_column = len(self.column_names)
        self.column_names_index = {}
        for iname in range(n_column):
            self.column_names_index[self.column_names[iname]] = iname
 
        target_vacancy_for_this_year.column_values = target_vacancy_for_this_year.get_multiple_attributes(self.column_names).reshape((-1, n_column))
        self.realestate_dataset.column_values = self.realestate_dataset.get_multiple_attributes(self.column_names).reshape((-1, n_column))
        self.proposal_component_set.column_values = self.proposal_component_set.get_multiple_attributes(self.column_names).reshape((-1, n_column))
        #defaults, can be changed later by spaces_variable specified in target_vacancy rates
        self.realestate_dataset.total_spaces = self.realestate_dataset[total_spaces_variable]
        self.proposal_component_set.total_spaces = self.proposal_component_set[total_spaces_variable]
        self.realestate_dataset.occupied_spaces = self.realestate_dataset[occupied_spaces_variable]
        
        self.accounting = {}; self.logging = {}
        #has_needed_components = zeros(self.proposal_set.size(), dtype='bool')
        for index in range(target_vacancy_for_this_year.size()):
            column_value = tuple(target_vacancy_for_this_year.column_values[index,:].tolist())
            accounting = {'target_vacancy': target_vacancy_for_this_year[target_vacancy.target_attribute_name][index]}
            if minimum_spaces_attribute in target_vacancy_for_this_year.get_known_attribute_names():
                accounting['minimum_spaces'] = target_vacancy_for_this_year[minimum_spaces_attribute][index]
            realestate_indexes = self.get_index_by_condition(self.realestate_dataset.column_values, column_value)
            component_indexes = self.get_index_by_condition(self.proposal_component_set.column_values, column_value)
            
            this_total_spaces_variable, this_occupied_spaces_variable = total_spaces_variable, occupied_spaces_variable
            ## total/occupied_spaces_variable can be specified either as a universal name for all realestate
            ## or in targe_vacancy_rate dataset for each vacancy category
            if occupied_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
                this_occupied_spaces_variable = target_vacancy_for_this_year[occupied_spaces_variable][index]
                self.realestate_dataset.occupied_spaces[realestate_indexes] = (self.realestate_dataset[this_occupied_spaces_variable][realestate_indexes]
                                                                               ).astype(self.realestate_dataset.occupied_spaces.dtype)
    
            if total_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
                this_total_spaces_variable = target_vacancy_for_this_year[total_spaces_variable][index]    
                self.realestate_dataset.total_spaces[realestate_indexes] = (self.realestate_dataset[this_total_spaces_variable][realestate_indexes]
                                                                            ).astype(self.realestate_dataset.total_spaces.dtype)
                self.proposal_component_set.total_spaces[component_indexes] = (self.proposal_component_set[this_total_spaces_variable][component_indexes]
                                                                               ).astype(self.proposal_component_set.total_spaces.dtype)
                
            accounting["total_spaces_variable"] = this_total_spaces_variable
            accounting["total_spaces"] = self.realestate_dataset.total_spaces[realestate_indexes].sum()
            accounting["occupied_spaces_variable"] = this_occupied_spaces_variable
            accounting["occupied_spaces"] = self.realestate_dataset.occupied_spaces[realestate_indexes].sum()
            accounting["target_spaces"] = int( round( accounting["occupied_spaces"] /\
                                                     (1 - accounting["target_vacancy"])
                                               ) )
            accounting["proposed_spaces"] = 0
            accounting["demolished_spaces"] = 0
            
            self.accounting[column_value] = accounting
            
            if self._is_target_reached(column_value):
                proposal_indexes = self.proposal_set.get_id_index(unique(self.proposal_component_set['proposal_id'][component_indexes]))
                if n_column == 1:
                    comp_indexes = where(ndimage.sum(self.proposal_component_set[self.column_names[0]]==column_value[0], 
                                    labels=self.proposal_component_set['proposal_id'], 
                                    index=self.proposal_set.get_id_attribute()
                                    ) == self.proposal_set["number_of_components"])[0]
                else:
                    comp_indexes = where(self.proposal_set["number_of_components"]==1)[0]
                target_reached_prop_idx = intersect1d(proposal_indexes, comp_indexes)
                self.weight[target_reached_prop_idx] = 0.0
                self.proposal_set["status_id"][intersect1d(target_reached_prop_idx, where(self.proposal_set["status_id"]==self.proposal_set.id_tentative)[0])] = self.proposal_set.id_no_demand
                
        ## handle planned proposals: all proposals with status_id == is_planned 
        ## and start_year == year are accepted
        planned_proposal_indexes = where(logical_and(
                                                  self.proposal_set.get_attribute("status_id") == self.proposal_set.id_planned, 
                                                  self.proposal_set.get_attribute("start_year") == year ) 
                                        )[0]
        
        logger.start_block("Processing %s planned proposals" % planned_proposal_indexes.size)
        self.consider_proposals(planned_proposal_indexes, force_accepting=True)
        logger.end_block()
        
        if within_parcel_selection_n > 0:
            logger.start_block("Selecting proposals within parcels (%s proposals per parcel)" % within_parcel_selection_n)
            self.select_proposals_within_parcels(nmax=within_parcel_selection_n, weight_string=within_parcel_selection_weight_string,
                                                 compete_among_types=within_parcel_selection_compete_among_types, 
                                                 filter_threshold=within_parcel_selection_threshold,
                                                 MU_same_weight=within_parcel_selection_MU_same_weight,
                                                 transpose_interpcl_weight=within_parcel_selection_transpose_interpcl_weight)
            logger.end_block()
        
        # consider proposals (in this order: proposed, tentative)
        for status in [self.proposal_set.id_proposed, self.proposal_set.id_tentative]:
            stat = (self.proposal_set.get_attribute("status_id") == status)
            if stat.sum() == 0:
                continue
            
            logger.log_status("Sampling from %s eligible proposals of status %s." % (stat.sum(), status))
            iteration = 0
            while (not self._is_target_reached()):
                ## prevent proposals from being sampled for vacancy type whose target is reached
                #for column_value in self.accounting.keys():
                
                if self.weight[stat].sum() == 0.0:
                    logger.log_warning("Running out of proposals of status %s before vacancy targets are reached; there aren't any proposals with non-zero weight" % status)
                    break
                
                available_indexes = where(logical_and(stat, self.weight > 0))[0]
                sample_size = minimum(available_indexes.size, n)
                sampled_proposal_indexes = probsample_noreplace(available_indexes, sample_size, 
                                                                prob_array=self.weight[available_indexes],
                                                                return_index=False)
                #sorted_sampled_indices = argsort(self.weight[sampled_proposal_indexes])
                #self.consider_proposals(sampled_proposal_indexes[sorted_sampled_indices][::-1])
                self.consider_proposals(sampled_proposal_indexes)
                self.weight[sampled_proposal_indexes] = 0
                iteration += 1
        
        self._log_status()
        
        # set status of accepted proposals to 'active'
        self.proposal_set.modify_attribute(name="status_id", 
                                           data=self.proposal_set.id_active,
                                           index=array(self.accepted_proposals, dtype='int32'))
        
        # Code added by Jesse Ayers, MAG, 7/20/2009
        # Get the active projects:
        stat_id = self.proposal_set.get_attribute('status_id')
        actv = where(stat_id==1)[0]
        # Where there are active projects, compute the total_land_area_taken
        # and store it on the development_project_proposals dataset
        # so it can be used by the building_construction_model for the proper
        # computation of units_proposed for those projects with velocity curves
        if actv.size > 0:          
            total_land_area_taken_computed = self.proposal_set['land_area_taken']
            self.proposal_set.modify_attribute('total_land_area_taken', total_land_area_taken_computed[actv], actv)

        return (self.proposal_set, self.realestate_dataset.get_id_attribute()[self.demolished_buildings])

    def _is_target_reached(self, column_value=()):
        if column_value:
            if self.accounting.has_key(column_value):
                accounting = self.accounting[column_value]
                result = (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                                accounting.get("demolished_spaces",0) )) and (
                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
                return result
            else:
                return True
        results = [  (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                            accounting.get("demolished_spaces",0) )) and (
                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
                   for column_value, accounting in self.accounting.items() ]
        return all(results)

    def select_proposals_within_parcels(self, nmax=2, weight_string=None, compete_among_types=False, filter_threshold=75, 
                                        MU_same_weight=False, transpose_interpcl_weight=True):
        # Allow only nmax proposals per parcel in order to not disadvantage parcels with small amount of proposals.
        # It takes proposals with the highest weights.
        #parcels_with_proposals = unique(self.proposal_set['parcel_id'])
        #parcel_set = self.dataset_pool.get_dataset('parcel')
        if weight_string is not None:
            within_parcel_weights = self.proposal_set.compute_variables([weight_string], dataset_pool=self.dataset_pool)
        else:
            within_parcel_weights = self.weight
        
        egligible = logical_and(self.weight > 0, 
                                self.proposal_set['status_id'] == self.proposal_set.id_tentative)
        wegligible = where(egligible)[0]
        if wegligible.size <=0:
            return
        #parcels_with_proposals = unique(self.proposal_set['parcel_id'][wegligible])
        #min_type = {}
        #egligible_proposals = {}
        tobechosen_ind = ones(wegligible.size).astype('bool8')
        if not compete_among_types:
            for key in self.column_names:
                utypes_all = unique(self.proposal_component_set[key])
                categories = zeros(self.proposal_set.size(), dtype='int32')
                for btype in utypes_all:
                    w = where(ndimage.sum(self.proposal_component_set[key] == btype,
                                          labels=self.proposal_component_set['proposal_id'], 
                                          index=self.proposal_set.get_id_attribute()
                                          ) == self.proposal_set["number_of_components"])[0]
                    categories[w] = btype
                # categories equal zero means mix-used type with components of different type

                utypes = unique(categories[wegligible])           
                for value in utypes:
                    type_is_value_ind = categories[wegligible]==value
                    for i in range(nmax):
                        parcels_with_proposals = (unique(self.proposal_set['parcel_id'][wegligible][where(type_is_value_ind)])).astype(int32)
                        if parcels_with_proposals.size <= 0:
                            continue
                        labels = (self.proposal_set['parcel_id'][wegligible])*type_is_value_ind               
                        chosen_prop = array(maximum_position(within_parcel_weights[wegligible], 
                                            labels=labels, 
                                            index=parcels_with_proposals)).flatten().astype(int32)               
                        egligible[wegligible[chosen_prop]] = False
                        type_is_value_ind[chosen_prop] = False
        else:
            parcels_with_proposals = unique(self.proposal_set['parcel_id'][wegligible]).astype(int32)
            max_prop = array(maximum_position(within_parcel_weights[wegligible], 
                                            labels=self.proposal_set['parcel_id'][wegligible], 
                                            index=parcels_with_proposals)).flatten().astype(int32)                                            
            max_value_by_parcel = within_parcel_weights[wegligible][max_prop]
            incompetition = ones(wegligible.size, dtype='bool8')
            incompetition[max_prop] = False
            egligible[wegligible[max_prop]] = False            
            for i in range(nmax-1):
                labels = (self.proposal_set['parcel_id'][wegligible])*incompetition 
                valid_parcels = where(in1d(parcels_with_proposals, self.proposal_set['parcel_id'][wegligible][where(incompetition)]))[0]
                if valid_parcels.size <= 0:
                    break
                chosen_prop = array(maximum_position(within_parcel_weights[wegligible], 
                                            labels=labels, 
                                            index=parcels_with_proposals[valid_parcels])).flatten().astype(int32)
                percent = within_parcel_weights[wegligible][chosen_prop]/(max_value_by_parcel[valid_parcels]/100.0)
                where_lower = where(in1d(self.proposal_set['parcel_id'][wegligible], parcels_with_proposals[valid_parcels][percent <= filter_threshold]))[0]
                egligible[wegligible[setdiff1d(chosen_prop, where_lower)]] = False   # proposals with egligible=True get eliminated, so we dont want to set it to False for the where_lower ones
                incompetition[union1d(chosen_prop, where_lower)] = False
                if incompetition.sum() <= 0:
                    break
             
            self.proposal_set['status_id'][where(egligible)] = self.proposal_set.id_eliminated_in_within_parcel_selection
            if MU_same_weight:
                # Set weights of mix-use proposals within the same parcel to the same value
                parcels = self.dataset_pool.get_dataset('parcel')
#                parcels.compute_variables(['mu_ind = parcel.aggregate(numpy.logical_or(development_project_proposal_component.building_type_id==4, development_project_proposal_component.building_type_id==12) + numpy.logical_or(development_project_proposal_component.building_type_id==3, development_project_proposal_component.building_type_id==13), intermediates=[development_project_proposal])'], 
#                                                    dataset_pool=self.dataset_pool)
#                pcl_ids = parcels.get_id_attribute()[parcels['mu_ind'] > 1]
#                is_mu = logical_and(logical_and(self.weight > 0, 
#                                self.proposal_set['status_id'] == self.proposal_set.id_tentative),
#                                       in1d(self.proposal_set['parcel_id'], pcl_ids))
#                where_mu = where(is_mu)[0]
#                if where_mu.size <= 0:
#                    return
#                trans_weights = self.weight[where_mu]
#                if transpose_interpcl_weight:
#                    trans_weights = log(trans_weights)
#                pcl_idx = parcels.get_id_index(self.proposal_set['parcel_id'][where_mu])
#                upcl_idx = unique(pcl_idx)
#                weight_mean = array(ndimage_mean(trans_weights, labels=pcl_idx,  index=upcl_idx))
#                if transpose_interpcl_weight:
#                    weight_mean = exp(weight_mean)
#                weight_mean_tmp = zeros(upcl_idx.max()+1).astype(weight_mean.dtype)
#                weight_mean_tmp[upcl_idx]=weight_mean
#                self.weight[where_mu]=weight_mean_tmp[pcl_idx]
                self.proposal_set.compute_variables(['is_mfres = development_project_proposal.aggregate(numpy.logical_or(development_project_proposal_component.building_type_id==4, development_project_proposal_component.building_type_id==12))'],
                                                    dataset_pool=self.dataset_pool)
                parcels.compute_variables(['mu_ind = (parcel.aggregate(development_project_proposal.is_mfres)>0) * (parcel.mix_split_id > 0)'], 
                                                    dataset_pool=self.dataset_pool)
                pcl_ids = parcels.get_id_attribute()[parcels['mu_ind'] > 0]
                egligible_props = logical_and(self.weight > 0, logical_and(
                                self.proposal_set['status_id'] == self.proposal_set.id_tentative,
                                self.proposal_set['is_mfres']>0))
                where_prop_to_modify = where(logical_and(egligible_props,
                                       in1d(self.proposal_set['parcel_id'], pcl_ids)))[0]
                if where_prop_to_modify.size <= 0:
                    return
                upcl = unique(self.proposal_set['parcel_id'][where_prop_to_modify])               
                npcl_to_modify = int(upcl.size/10.0)
                if npcl_to_modify == 0:
                    return
                pcls_to_modify = sample_noreplace(upcl, npcl_to_modify)
                where_prop_to_modify_final = where(logical_and(egligible_props,
                                       in1d(self.proposal_set['parcel_id'], pcls_to_modify)))[0]
                trans_weights = self.weight[where_prop_to_modify_final]
                if transpose_interpcl_weight:
                    trans_weights = log(trans_weights)
                trans_weights = 1.2*trans_weights
                if transpose_interpcl_weight:
                    trans_weights = exp(trans_weights)
                self.weight[where_prop_to_modify_final] = trans_weights
                return
            