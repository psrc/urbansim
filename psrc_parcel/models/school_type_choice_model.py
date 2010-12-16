from opus_core.choice_model import ChoiceModel
from opus_core.datasets.dataset import Dataset
from urbansim.datasets.household_dataset import HouseholdDataset

class SchoolTypeChoiceModel(ChoiceModel):
    def prepare_for_estimate(self, estimation_storage, agents_for_estimation_table, agent_set, 
                             households_for_estimation_table=None, **kwargs):
        estimation_set = Dataset(in_storage = estimation_storage,
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
        if households_for_estimation_table is not None:
            hhs = HouseholdDataset(in_storage=estimation_storage, in_table_name='households_for_estimation')
            self.dataset_pool.replace_dataset('household', hhs)
        spec, index = ChoiceModel.prepare_for_estimate(self, estimation_set, **kwargs)
        return (spec, index, estimation_set)