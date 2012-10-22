# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.models.development_project_proposal_sampling_model_with_minimum import DevelopmentProjectProposalSamplingModel as DevelopmentProjectProposalSamplingModelWithMinimum
from opus_core.datasets.dataset import DatasetSubset
from opus_core.simulation_state import SimulationState
from numpy import where

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
        if column_value:
            results = [  (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                            accounting.get("demolished_spaces",0) )) and (
                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
                   for column_value, accounting in self.accounting.items() if column_value[0] in self.same_demand_group]
        else:
            results = [  (accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                            accounting.get("demolished_spaces",0) )) and (
                         accounting.get("proposed_spaces",0) >= accounting.get("minimum_spaces",0))
                   for column_value, accounting in self.accounting.items() ]
        return all(results)         
                



