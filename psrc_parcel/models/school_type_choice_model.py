# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import zeros, logical_and, where
from opus_core.choice_model import ChoiceModel
from opus_core.hierarchical_choice_model import HierarchicalChoiceModel
from opus_core.datasets.dataset import Dataset
from opus_core.misc import ismember
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim_parcel.datasets.person_dataset import PersonDataset

class SchoolTypeChoiceModel(ChoiceModel):
    def prepare_for_estimate(self, estimation_storage, agents_for_estimation_table, agent_set, 
                             households_for_estimation_table=None, **kwargs):
        estimation_set = Dataset(in_storage = estimation_storage,
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
        if households_for_estimation_table is not None:
            hhs = HouseholdDataset(in_storage=estimation_storage, in_table_name=households_for_estimation_table)
            self.dataset_pool.replace_dataset('household', hhs)
        self.dataset_pool.replace_dataset(estimation_set.get_dataset_name(), estimation_set)
        spec, index = ChoiceModel.prepare_for_estimate(self, estimation_set, **kwargs)
        return (spec, index, estimation_set)
    
    def prepare_for_estimate_hh(self, estimation_storage, agents_for_estimation_table, agent_set, 
                             persons_for_estimation_table=None, **kwargs):
        estimation_set = Dataset(in_storage = estimation_storage,
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
        if persons_for_estimation_table is not None:
            pers = PersonDataset(in_storage=estimation_storage, in_table_name=persons_for_estimation_table)
            self.dataset_pool.replace_dataset('person', pers)
        self.dataset_pool.replace_dataset(estimation_set.get_dataset_name(), estimation_set)
        spec, index = ChoiceModel.prepare_for_estimate(self, estimation_set, **kwargs)
        return (spec, index, estimation_set)
    
    def run(self, specification, coefficients, agent_set, agents_index=None, sync_persons=False, **kwargs):
        """Set sync_persons to True if the model is run on households level and the persons table 
        should be synchronized. 
        """       
        results = ChoiceModel.run(self, specification, coefficients, agent_set, agents_index=None, **kwargs)
        if sync_persons:
            persons = self.dataset_pool.get_dataset('person')
            choice_id_name = self.choice_set.get_id_name()[0]
            values = persons.compute_variables(
                    ['_tmp_ = person.disaggregate(%s.%s)' % (agent_set.get_dataset_name(), 
                                                             choice_id_name)], 
                                               dataset_pool=self.dataset_pool)
            if agents_index==None:
                agents_index=arange(agent_set.size())
            pers_idx = ismember(persons['%s' % agent_set.get_id_name()[0]], agent_set.get_id_attribute()[agents_index])
            if choice_id_name not in persons.get_known_attribute_names():
                persons.add_primary_attribute(data=zeros(persons.size(), dtype=values.dtype), name=choice_id_name)
            persons.modify_attribute(data=values, name=choice_id_name, index=pers_idx)
            persons.delete_one_attribute('_tmp_')
        return results
    
    def prepare_for_run(self, agent_set=None, agent_filter=None, agents_index=None, filter_threshold=0, **kwargs):
        """Combine agent_filter and agents_index."""
        spec, coef, index = ChoiceModel.prepare_for_run(self, agent_set=agent_set, agent_filter=agent_filter, 
                                    filter_threshold=filter_threshold, **kwargs)
        if agents_index is not None:
            tmp1 = zeros(agent_set.size(), dtype='bool8')
            tmp1[agents_index] = True
            if index is not None:
                tmp2 = zeros(agent_set.size(), dtype='bool8')
                tmp2[index] = True
                tmp1 = logical_and(tmp1, tmp2)
            index = where(tmp1)[0]
        return (spec, coef, index)
    
class SchoolTypeChoiceModelNested(HierarchicalChoiceModel):
    def prepare_for_estimate(self, estimation_storage, agents_for_estimation_table, agent_set, 
                             households_for_estimation_table=None, **kwargs):
        estimation_set = Dataset(in_storage = estimation_storage,
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
        if households_for_estimation_table is not None:
            hhs = HouseholdDataset(in_storage=estimation_storage, in_table_name='households_for_estimation')
            self.dataset_pool.replace_dataset('household', hhs)
        self.dataset_pool.replace_dataset(estimation_set.get_dataset_name(), estimation_set)
        spec, index = HierarchicalChoiceModel.prepare_for_estimate(self, estimation_set, **kwargs)
        return (spec, index, estimation_set)