# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import re
from numpy import arange, array, resize
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults, Resources
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel

class AgentLocationChoiceModelMember(AgentLocationChoiceModel):
    """It sets the AgentLocationChoiceModel as a member of a model group."""

    def __init__(self, group_member, location_set,
            agents_grouping_attribute, model_name, short_name, **kwargs):
        """ 'group_member' is of type ModelGroupMember. 'agents_grouping_attribute' is attribute of the agent_set
        (passed to the 'run' and 'estimate' method) that is used for grouping.
        """
        self.group_member = group_member
        group_member_name = group_member.get_member_name()
        self.group_member.set_agents_grouping_attribute(agents_grouping_attribute)

        AgentLocationChoiceModel.__init__(self, location_set,
                                        model_name = "%s %s" % (group_member_name.capitalize(), model_name),
                                        short_name = "%s %s" % (group_member_name.capitalize(), short_name),
                                        **kwargs)

    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        data_objects = kwargs.get("data_objects",{})
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        # filter out agents for this group
        new_agents_index = self.group_member.get_index_of_my_agents(agent_set, agents_index, dataset_pool=self.dataset_pool)
        choices = AgentLocationChoiceModel.run(self,  specification, coefficients, agent_set,
                                               agents_index=agents_index[new_agents_index], **kwargs)
        result = resize(array([-1], dtype=choices.dtype), agents_index.size)
        result[new_agents_index] = choices
        return result

    def estimate(self, specification, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        # filter out agents for this group
        new_agents_index = self.group_member.get_index_of_my_agents(agent_set, agents_index)
        return AgentLocationChoiceModel.estimate(self,  specification, agent_set,
                                               agents_index=agents_index[new_agents_index], **kwargs)

    def prepare_for_run(self, add_member_prefix=True, specification_storage=None, specification_table=None, coefficients_storage=None,
                         coefficients_table=None, **kwargs):
        if add_member_prefix:
            specification_table, coefficients_table = \
                self.group_member.add_member_prefix_to_table_names([specification_table, coefficients_table])

        return AgentLocationChoiceModel.prepare_for_run(self, specification_storage=specification_storage, specification_table=specification_table, 
                                                        coefficients_storage=coefficients_storage, coefficients_table=coefficients_table, **kwargs)

    def prepare_for_estimate(self, add_member_prefix=True, specification_dict=None, specification_storage=None,
                             specification_table=None, **kwargs):
        if add_member_prefix:
            specification_table = self.group_member.add_member_prefix_to_table_name(specification_table)
        if 'movers_variable' in kwargs.keys():
            kwargs['movers_variable'] = re.sub('SSS', self.group_member.get_member_name(), kwargs['movers_variable'])
        return AgentLocationChoiceModel.prepare_for_estimate(self, specification_dict, specification_storage, specification_table, **kwargs)