# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.models.development_project_proposal_sampling_model_with_minimum import DevelopmentProjectProposalSamplingModel as DevelopmentProjectProposalSamplingModelWithMinimum
from opus_core.datasets.dataset import DatasetSubset
from opus_core.simulation_state import SimulationState
from numpy import where, intersect1d, in1d, array, unique
from scipy.ndimage import maximum
from collections import defaultdict

class DevelopmentProjectProposalSamplingModel(DevelopmentProjectProposalSamplingModelWithMinimum):
    """
    The demand of building types given by same_demand_group is considered jointly, i.e. those types are built until 
    the vacancy of all those types is met (this addresses an issue with a timing of development).
    """
      
    same_demand_group = [3, 13, 4, 12]
    def run(self, n=500, 
            realestate_dataset_name = 'building',
            current_year=None,
            **kwargs):

        target_vacancy = self.dataset_pool.get_dataset('target_vacancy')

        if current_year is None:
            year = SimulationState().get_current_time()
        else:
            year = current_year
        self.current_year = year
        this_year_index = where(target_vacancy['year']==year)[0]
        target_vacancy_for_this_year = DatasetSubset(target_vacancy, this_year_index)
        if target_vacancy_for_this_year.size() == 0:
            raise IOError, 'No target vacancy defined for year %s.' % year
        self.all_btypes_size = target_vacancy_for_this_year.size()
        return DevelopmentProjectProposalSamplingModelWithMinimum.run(self, n=n, realestate_dataset_name=realestate_dataset_name,
                                                                      current_year=current_year, **kwargs)
        
    def _is_target_reached(self, column_value=()):
        if column_value and column_value[0] not in self.same_demand_group:
            return DevelopmentProjectProposalSamplingModelWithMinimum._is_target_reached(self, column_value)
        if len(self.accounting) < self.all_btypes_size:
            return False
        return DevelopmentProjectProposalSamplingModelWithMinimum._is_target_reached(self, column_value)
#        if column_value:
#            is_target_reached = DevelopmentProjectProposalSamplingModelWithMinimum._is_target_reached(self, column_value)
#            results = [  (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
#                                                            accounting.get("demolished_spaces",0) )) and (
#                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
#                   for column_value, accounting in self.accounting.items() if column_value[0] in self.same_demand_group]
#        else:
#            results = [  (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
#                                                            accounting.get("demolished_spaces",0) )) and (
#                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
#                   for column_value, accounting in self.accounting.items() ]
#        return all(results)      
    
    def _are_targets_reached(self, column_value):
        if (column_value[0] not in self.same_demand_group) or (self.current_year >= 2015):
            return (DevelopmentProjectProposalSamplingModelWithMinimum._is_target_reached(self, column_value), True)
        is_target_reached = DevelopmentProjectProposalSamplingModelWithMinimum._is_target_reached(self, column_value)
        results = [  (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                            accounting.get("demolished_spaces",0) )) and (
                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
                   for column_value, accounting in self.accounting.items() if column_value[0] in self.same_demand_group]
        return (is_target_reached, all(results))            
                

    def consider_proposal(self, proposal_index, force_accepting=False):
        if self.weight[proposal_index] <= 0:
            return False
        this_site = self.proposal_set["parcel_id"][proposal_index]            
        building_indexes = array([], dtype='i')
        demolished_spaces = defaultdict(int)
        if self.proposal_set["is_redevelopment"][proposal_index] or force_accepting:  #redevelopment proposal
            building_indexes = where(self.realestate_dataset['parcel_id']==this_site)[0]
            for building_index in building_indexes:
                column_value = tuple(self.realestate_dataset.column_values[building_index,:].tolist())
                demolished_spaces[column_value] += self.realestate_dataset.total_spaces[building_index]

        component_indexes = where(self.proposal_component_set['proposal_id']==self.proposal_set['proposal_id'][proposal_index])[0]
        proposed_spaces = defaultdict(int) 
        #[(self.proposal_component_set.column_values[component_index,:], self.proposal_component_set.total_spaces[component_indexes])]            
        for component_index in component_indexes:
            column_value = tuple(self.proposal_component_set.column_values[component_index,:].tolist())
            proposed_spaces[column_value] += self.proposal_component_set.total_spaces[component_index]
        
        ## skip this proposal if the proposal has no components that are needed to reach vacancy target
        if not force_accepting and all([ self._is_target_reached(key) 
                 or (proposed_spaces.get(key,0) - demolished_spaces.get(key,0) <= 0)  ## 
                 for key in proposed_spaces.keys() ]):
            return False
        
        # accept this proposal
        for key, value in demolished_spaces.items():
            if key not in self.accounting:
                if key not in self.logging:
                    self.logging[key] = defaultdict(int)
                self.logging[key]["demolished_spaces"] += value
            else:
                self.accounting[key]["demolished_spaces"] += value 
                ##TODO we may want to re-activate sampling of proposals if new total spaces is below target spaces 
                ##because of demolished buildings 
        
        for key, value in proposed_spaces.items():
            if key not in self.accounting:
                if key not in self.logging:
                    self.logging[key] = defaultdict(int)
                self.logging[key]["proposed_spaces"] += value
            else:
                self.accounting[key]["proposed_spaces"] += value
                targets_reached = self._are_targets_reached(key)
                if targets_reached[0]:
                    component_indexes = self.get_index_by_condition(self.proposal_component_set.column_values, key)
                    proposal_indexes = self.proposal_set.get_id_index( unique(self.proposal_component_set['proposal_id'][component_indexes]) )
                    if not targets_reached[1]:
                        # disable proposals for all parcels with proposals of this BT 
                        proposal_indexes = intersect1d(where(self.get_index_by_condition(self.proposal_set['status_id'], self.proposal_set.id_tentative))[0], proposal_indexes)  
                        parcels = self.proposal_set['parcel_id'][proposal_indexes]
         #               btonpcl = zeros(parcels.size)
         #               for bt in target_vacancy_for_this_year['building_type_id']:
         #                   btonpcl =  btonpcl + array(maximum(self.proposal_component_set['building_type_id'] == bt, labels=parcels, index=parcels))
                            
         #               parcels = parcels[btonpcl>=3]
                        proposal_indexes = where(in1d(self.proposal_set['parcel_id'], parcels))[0]
                    self.weight[proposal_indexes] = 0.0
                                     
        if building_indexes.size > 0: self.demolished_buildings.extend(building_indexes.tolist())
        self.accepted_proposals.append(proposal_index)
        
        # don't consider proposals for this site in future sampling
        self.weight[proposal_index] = 0.0
        self.weight[self.proposal_set["parcel_id"] == this_site] = 0.0
        return True


