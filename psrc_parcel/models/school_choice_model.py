# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.datasets.dataset import Dataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.models.location_choice_model import LocationChoiceModel

class SchoolChoiceModel(LocationChoiceModel):
    def prepare_for_estimate(self, estimation_storage, agents_for_estimation_table, agent_set, 
                             households_for_estimation_table=None, **kwargs):
        estimation_set = Dataset(in_storage = estimation_storage,
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
        self.dataset_pool.replace_dataset('person', estimation_set)
        if households_for_estimation_table is not None:
            hhs = HouseholdDataset(in_storage=estimation_storage, in_table_name='households_for_estimation')
            self.dataset_pool.replace_dataset('household', hhs)
        spec, index = LocationChoiceModel.prepare_for_estimate(self, estimation_set, **kwargs)
        return (spec, index, estimation_set)
