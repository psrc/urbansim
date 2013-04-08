# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import unique, where, maximum, zeros, apply_along_axis, newaxis, logical_and
from opus_core.datasets.dataset import Dataset
from opus_core.logger import logger
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel

class SchoolChoiceModel(AgentLocationChoiceModel):
    model_name = 'School Location Choice Model'
                
    def prepare_for_estimate(self, estimation_storage, agents_for_estimation_table, agent_set, 
                             households_for_estimation_table=None, **kwargs):
        estimation_set = Dataset(in_storage = estimation_storage,
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
        self.dataset_pool.replace_dataset('person', estimation_set)
        if households_for_estimation_table is not None:
            hhs = HouseholdDataset(in_storage=estimation_storage, in_table_name='households_for_estimation')
            self.dataset_pool.replace_dataset('household', hhs)
        spec, index = AgentLocationChoiceModel.prepare_for_estimate(self, estimation_set, **kwargs)
        return (spec, index, estimation_set)
    
    def create_interaction_datasets(self, agent_set, agents_index, config, submodels=[-2], **kwargs):
        """Like the parent method but it also deals with filtering by groups.
        """
        def mywhere(x, index): 
            i = where(index == x)[0]
            if i.size == 0:
                i=-1
            return i
	
        nchoices = self.get_choice_set_size()
        if nchoices <> self.choice_set.size() or self.filter is None:
            return AgentLocationChoiceModel.create_interaction_datasets(self, agent_set, agents_index, config, submodels, **kwargs)
        
        # apply filter without doing sampling

        groups = [-2]
        group_values = None
        if config.get("filter_by_groups", False):
            group_var = config.get("group_definition_for_filtering_alternatives", None)
            if group_var is None:
                raise 'No group variable defined for filtering alternatives. Set "group_definition_for_filtering_alternatives" in run_config/estimate_config.'
            else:
                group_values = agent_set.compute_variables([group_var], dataset_pool=self.dataset_pool)[agents_index]
                groups = unique(group_values)


        where_group = {}
        choice_index = {}
        chosen_choice = {}
        maxsize = 0
        for submodel in submodels:
            where_submodel = self.observations_mapping[submodel]
            is_submodel = zeros(agents_index.size, dtype='bool8')
            is_submodel[where_submodel] = True
            for group in groups:
                if group_values is None:
                    where_group[(submodel, group)] = where_submodel
                else:
                    where_group[(submodel, group)] = where(logical_and(group_values == group, is_submodel))[0]
                if where_group[(submodel, group)].size==0:
                    continue
                agents_index_in_group = agents_index[where_group[(submodel, group)]]
                choice_index[(submodel, group)] = self.apply_filter(self.filter, agent_set=agent_set, 
                                                 agents_index=agents_index_in_group,  
                                                 submodel=submodel, 
                                                 replace_dict={'SUBMODEL': submodel, 'GROUP': group})
                if choice_index[(submodel, group)] is not None and choice_index[(submodel, group)].size == 0:
                    logger.log_error("There is no alternative that passes filter %s for SUBMODEL=%s and GROUP=%s; %s agents with id %s will remain unplaced." % \
                                     (self.filter, submodel, group, agents_index_in_group.size, agent_set.get_id_attribute()[agents_index_in_group]))
                    continue
                if config.get('include_chosen_choice', False):
                    chosen = self.choice_set.get_id_index(id=agent_set.get_attribute_by_index(self.choice_set.get_id_name()[0],
                                                                                                       agents_index_in_group))
                    chosen_choice[(submodel, group)] = apply_along_axis(mywhere, 1, chosen[:,newaxis], choice_index[(submodel, group)])
                maxsize = maximum(maxsize, choice_index[(submodel, group)].size)
                
        filter_index = -1 + zeros((agents_index.size, maxsize), dtype="int32")
        for submodel, group in choice_index.keys():    
            filter_index[where_group[(submodel, group)],0:choice_index[(submodel, group)].size] = choice_index[(submodel, group)][newaxis, :].repeat(where_group[(submodel, group)].size, axis=0)
        self.model_interaction.create_interaction_datasets(agents_index, filter_index)
        
        if config.get('include_chosen_choice', False):
            chosen_choice_attr = zeros((agents_index.size, maxsize), dtype="bool8")
            for submodel, group in chosen_choice.keys():  
                chosen_choice_attr[where_group[(submodel, group)], chosen_choice[(submodel, group)].flat] = True
            self.model_interaction.interaction_dataset.add_attribute(data=chosen_choice_attr, name="chosen_choice")
                    
        self.update_choice_set_size(maxsize)
        return

