# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.models.choice_model import ChoiceModel
from opus_core.datasets.dataset import Dataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel

class PersonLocationChoiceModel(AgentLocationChoiceModel):
    """Can be used for location choice models where persons are agents. 
        For estimation, it replaces persons and households tables in dataset_pool by 
        persons_for_estimation and household_for_estimation tables.
    """  
                
    def prepare_for_estimate(self, agents_for_estimation_storage, agents_for_estimation_table, agent_set, **kwargs):
        estimation_set = Dataset(in_storage = agents_for_estimation_storage,
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
        hhs_est = HouseholdDataset(in_storage=agents_for_estimation_storage, in_table_name='households_for_estimation')
        self.dataset_pool.replace_dataset('household', hhs_est)
        self.dataset_pool.replace_dataset(estimation_set.get_dataset_name(), estimation_set)
        spec, index = ChoiceModel.prepare_for_estimate(self, estimation_set, **kwargs)        
        return (spec, index, estimation_set)
